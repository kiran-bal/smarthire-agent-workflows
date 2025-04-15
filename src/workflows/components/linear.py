"""
Contains the class for the linear workflow graph creation
"""

from src.workflows.components import BaseWorkflow


class LinearWorkflow(BaseWorkflow):
    """
    Class for the linear workflow creation
    """

    def build_graph(self):
        """
        Builds the graph using the linear nodes.
        This graph will have a sequential execution order
        without conditions.

        Returns: None
        """
        # Add nodes to the graph
        for node_config in self.config["nodes"]:
            node_name = node_config["name"]
            node = self.node_factory.create_node(node_name, node_config)
            self.graph.add_node(node_name, node.execute)

        # Add edges to the graph
        for edge in self.config.get("edges", []):
            from_node = edge["from_node"]
            next_node = edge["next_node"]
            self.graph.add_edge(from_node, next_node)
