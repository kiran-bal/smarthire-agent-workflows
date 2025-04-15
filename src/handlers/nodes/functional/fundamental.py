from constants import CURR_EXECUTION_NODE_KEY
from src.handlers.nodes.base import BaseNodeHandler
from utils.log_message import custom_log


class FundamentalNodeHandler(BaseNodeHandler):
    def __init__(self, config: dict, method=None):
        self.config = config
        self.method = method
        super().__init__(config)

    def execute(self, state):
        if hasattr(self, self.method):
            func = getattr(self, self.method)
            return func(state)
        raise AttributeError(
            f"Method '{self.method}' not found in {self.__class__.__name__}"
        )

    def check_node_output(self, state):
        curr_execution_node = state.get(CURR_EXECUTION_NODE_KEY)
        curr_output_field = self.config[curr_execution_node].get("output_field")
        node_output = state.get(curr_output_field)
        if node_output:
            custom_log("## Node execution success")
            return "continue"
        else:
            custom_log("## No node execution result")
            return "end"

    @staticmethod
    def stop_execution(state):
        custom_log("## Stopping the current execution")
        return state
