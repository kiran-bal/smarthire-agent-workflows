"""
Contains the class for the conditional workflow graph creation
"""

from src.workflows.components import BaseWorkflow
from src.handlers.nodes.functional.fundamental import FundamentalNodeHandler


class ConditionalWorkflow(BaseWorkflow):
    """
    Class for the conditional workflow creation
    """

    def build_graph(self):
        """
        Builds the graph using the conditional nodes
        This graph will have a sequential execution order and
        condition to navigate to other nodes
        Returns: NA

        """
        node_configuration = self.node_factory.config
        for node_config in self.config["nodes"]:
            node_name = node_config["name"]
            node = self.node_factory.create_node(node_name, node_config)
            self.graph.add_node(node_name, node.execute)

        for condition in self.config.get("conditions", []):
            condition_method = getattr(
                FundamentalNodeHandler(config=node_configuration, method=condition["condition"]), "execute"
            )
            self.graph.add_conditional_edges(
                condition["from_node"], condition_method, condition["paths"]
            )
