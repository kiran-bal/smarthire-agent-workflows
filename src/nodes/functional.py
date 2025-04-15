"""
Contains the class to create and execute the functional nodes
"""

import importlib

from constants import (
    CURR_EXECUTION_NODE_KEY,
    NODE_HANDLER_MODULE_PATH_KEY,
    NODE_AGENTS_KEY,
    NODE_MODULE_KEY,
    NODE_METHOD_KEY,
    PREV_EXECUTION_NODE_KEY,
    NODE_INPUTS_KEY,
    NODE_OUTPUT_FIELD_KEY,
)
from src.handlers.nodes.base import BaseNodeHandler
from src.nodes.base import BaseNode
from src.entities.states import WorkflowGraphState
from utils.log_message import custom_log


class FunctionalNode(BaseNode):
    """
    Creates and executes functional nodes
    """

    def __init__(self, config, agent_factory, task_factory, node_name):
        super().__init__(config, agent_factory, task_factory)
        self.node_name = node_name

    def execute(self, state: dict) -> WorkflowGraphState:
        """
        Executes the functional node and saves the state information
        Args:
            state: lang graph state for current execution

        Returns:
            WorkflowGraphState: Updated lang graph state for current execution
        """
        custom_log("Executing FunctionalNode")
        state[PREV_EXECUTION_NODE_KEY] = state.get(CURR_EXECUTION_NODE_KEY)
        state[CURR_EXECUTION_NODE_KEY] = self.node_name
        crew_config = self.config.get(self.node_name)
        # TODO: Update here for node execution
        inputs = crew_config.get("inputs")
        inputs = inputs if inputs else {}

        agent = self.__get_agent()
        class_name = agent.get(NODE_MODULE_KEY)
        method_name = agent.get(NODE_METHOD_KEY)

        node = self.__create_node(class_name=class_name, method_name=method_name)
        result = node.execute(state={**state, **inputs})  # Execute the node
        # TODO: Update only the key after the single assignment
        state= result if result else state
        return state

    def __create_node(self, class_name: str, method_name: str) -> BaseNodeHandler:
        """
        Retrieve the functional node from the handler nodes path
        and get method from the given module name (class).
        Args:
            class_name: Name of the class instance to be created
        Returns:
            Callable: callable method based on the configuration
        """
        handler_module_path = NODE_HANDLER_MODULE_PATH_KEY
        try:
            # Dynamically import the module
            module = importlib.import_module(handler_module_path)

            # Get the class from the module
            handler_class = getattr(module, class_name)
            instance = handler_class(config=self.config, method=method_name)

            return instance

        except ImportError as e:
            raise f"Error importing module {handler_module_path}: {e}"
        except AttributeError as e:
            raise f"Error finding class {class_name} in module {handler_module_path}: {e}"

    def __get_agent(self):
        """
        Retrieves the agent from the configuration
        for the current node
        Returns:
            agent: current agent for the node
        """
        agent = self.config[self.node_name].get(NODE_AGENTS_KEY)
        if not agent:
            raise Exception(f"Node {self.node_name} not available in the templates")
        agent_name = agent[0]
        agent = self.agent_factory.config.get(agent_name)
        return agent
