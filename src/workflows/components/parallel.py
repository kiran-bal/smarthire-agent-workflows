"""
Contains the class for the parallel workflow graph creation
"""

from src.workflows.components import BaseWorkflow


class ParallelWorkflow(BaseWorkflow):
    """
    Parallel workflow: nodes listed together in an edge run concurrently.

    Edges accept a string or a list on either side. A list on ``next_node``
    fans out; a list on ``from_node`` fans in, and LangGraph waits for every
    listed node before continuing.

        edges:
          - {from_node: extract, next_node: [questions, summary]}
          - {from_node: [questions, summary], next_node: send_email}
    """

    def build_graph(self):
        for node_config in self.config["nodes"]:
            node_name = node_config["name"]
            node = self.node_factory.create_node(node_name, node_config)
            self.graph.add_node(node_name, self.as_delta(node.execute))

        for edge in self.config.get("edges", []):
            sources = edge["from_node"]
            targets = edge["next_node"]
            sources = sources if isinstance(sources, list) else [sources]
            targets = targets if isinstance(targets, list) else [targets]
            for target in targets:
                if len(sources) > 1:
                    self.graph.add_edge(sources, target)  # fan-in: wait for all
                else:
                    self.graph.add_edge(sources[0], target)
