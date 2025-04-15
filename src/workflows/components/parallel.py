"""
Contains the class for the parallel workflow graph creation
"""

from src.workflows.components import BaseWorkflow


class ParallelWorkflow(BaseWorkflow):
    """
    Class for the parallel workflow creation
    """

    def build_graph(self):
        """
        Builds the graph using the parallel nodes
        parallel workflow is not implemented
        Returns: NA

        """
        for node_config in self.config["nodes"]:
            node_name = node_config["name"]
            node = self.node_factory.create_node(node_name, node_config)
            self.graph.add_parallel_node(node_name, node.execute)
