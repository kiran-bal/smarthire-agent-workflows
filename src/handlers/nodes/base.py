"""
Contains abstract base class to manage the Node handler functionalities
"""

from abc import ABC, abstractmethod

from constants import CURR_EXECUTION_NODE_KEY
from utils.log_message import custom_log


class BaseNodeHandler(ABC):
    """
    Abstract base class for the Node handler
    """

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def execute(self, state):
        """Abstract method to build the graph based on workflow type"""
        pass

    def check_node_output(self, state):
        """
        Checks the node output using the previous node result
        Args:
            state: must contain the state variables
        Returns:
            continue -> if the node_output is available else end
        """
        curr_execution_node = state.get(CURR_EXECUTION_NODE_KEY)
        curr_output_field = self.config[curr_execution_node].get("output_field")
        node_output = state.get(curr_output_field)
        if node_output:
            custom_log("## Node execution success")
            return "continue"
        else:
            custom_log("## No node execution result")
            return "end"
