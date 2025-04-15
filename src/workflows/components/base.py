"""
Contains abstract base class to manage the workflows
"""

from abc import ABC, abstractmethod
from typing import Union, List, Dict
from langgraph.graph import StateGraph

from constants import CURR_EXECUTION_NODE_KEY, PREV_EXECUTION_NODE_KEY, LAST_NODE_OUTPUT_KEY, CURRENT_DATETIME_KEY
from src.entities.states.state_builder import DynamicTypedDictBuilder
from src.nodes.node_factory import NodeFactory


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

        workflow_state = DynamicTypedDictBuilder.create_typeddict(
            name="WorkFlowState", fields=state_fields
        )
        return workflow_state
