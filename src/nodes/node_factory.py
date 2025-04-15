"""
Contains the classes for managing the nodes
"""

from src.agents.agent_factory import AgentFactory
from src.nodes.ai import AINode
from src.nodes.crew import CrewNode
from src.nodes.functional import FunctionalNode


class NodeFactory:
    """
    Factory class to manage the nodes
    """

    def __init__(self, config, agent_factory: AgentFactory, task_factory):
        self.config = config
        self.agent_factory = agent_factory
        self.task_factory = task_factory

    def create_node(self, node_name: str, node_config: dict):
        """
        Create a node based on the node type specified in the configuration.
        Args:
            node_name: The name of the node
            node_config: configuration for node creation
        Returns:
            Instance of a specific node type
        """

        node_type = node_config.get("type")
        if node_type == "crew":
            return CrewNode(
                self.config, self.agent_factory, self.task_factory, node_name
            )
        elif node_type == "functional":
            return FunctionalNode(
                self.config, self.agent_factory, self.task_factory, node_name
            )
        elif node_type == "ai":
            return AINode(self.config, self.agent_factory, self.task_factory)

        raise ValueError(f"Unknown node type: {node_type}")
