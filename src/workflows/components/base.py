"""
Contains abstract base class to manage the workflows
"""

from abc import ABC, abstractmethod
from typing import Annotated, Any, Union, List, Dict
from langgraph.graph import StateGraph

from constants import CURR_EXECUTION_NODE_KEY, PREV_EXECUTION_NODE_KEY, LAST_NODE_OUTPUT_KEY, CURRENT_DATETIME_KEY
from src.entities.states.state_builder import DynamicTypedDictBuilder
from src.nodes.node_factory import NodeFactory


def last_writer_wins(_current: Any, incoming: Any) -> Any:
    """
    State reducer: keep the most recent value.

    LangGraph refuses concurrent writes to a plain key. Parallel branches all
    update the bookkeeping keys (current node, last output), so every field is
    declared with this reducer. Branches that run in parallel should still
    write their results to *distinct* output fields; for a shared key the
    last branch to finish wins.
    """
    return incoming


class BaseWorkflow(ABC):
    """
    Abstract base class for the workflows
    """

    def __init__(self, config, node_factory: NodeFactory):
        self.config = config
        self.node_factory = node_factory
        workflow_state = self.build_state()
        self.graph = StateGraph(workflow_state)

    @abstractmethod
    def build_graph(self):
        """Abstract method to build the graph based on workflow type"""
        pass

    @staticmethod
    def as_delta(execute):
        """
        Wrap a node's ``execute`` so the graph receives only the keys it changed.

        Nodes are written to mutate and return the whole state, which is fine
        in a linear graph but makes parallel branches overwrite each other's
        results with stale copies. Returning a delta lets LangGraph merge
        branches key by key.
        """

        def run(state):
            before = dict(state)
            after = execute(dict(state))
            if after is None:
                return {}
            return {k: v for k, v in after.items() if k not in before or before[k] != v}

        return run

    def set_entry_and_finish(self, entry_point: str, finish_point: str):
        """
        Set the entry and finish points for the graph
        Args:
            entry_point: unique string for the entry point node
            finish_point: unique string for the finish point of node
        """
        self.graph.set_entry_point(entry_point)
        self.graph.set_finish_point(finish_point)

    def compile(self):
        """
        compiles the workflow graph defined
        Returns: compiled graph

        """
        return self.graph.compile()

    def build_state(self):
        """
        Builds the required state fields by looking at the workflow configuration and
        extracting the corresponding state fields from the nodes configuration.

        Returns:
            graph state generated from the nodes in workflow
        """
        node_config = self.node_factory.config
        node_states_map = {
            node_name: node_data.get("state_fields", {})
            for node_name, node_data in node_config.items()
        }
        workflow_nodes = [node["name"] for node in self.config.get("nodes")]

        state_fields = {
            CURR_EXECUTION_NODE_KEY: str,
            PREV_EXECUTION_NODE_KEY: str,
            LAST_NODE_OUTPUT_KEY: Union[str, List[str], Dict[str, str]],
            CURRENT_DATETIME_KEY: str
        }

        for node_name in workflow_nodes:
            if node_name in node_states_map:
                if node_name != "stop_execution":
                    for field, field_type in node_states_map[node_name].items():
                        state_fields.update(
                            {field: field_type}
                        )  # Initialize fields with None
            else:
                raise ValueError(
                    f"Node '{node_name}' found in workflow "
                    f"but not defined in nodes configuration."
                )

        annotated = {name: Annotated[field_type, last_writer_wins] for name, field_type in state_fields.items()}
        workflow_state = DynamicTypedDictBuilder.create_typeddict(
            name="WorkFlowState", fields=annotated
        )
        return workflow_state
