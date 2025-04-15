"""
Contains the abstract class for the Nodes
"""

from abc import ABC, abstractmethod


# Base abstract class for nodes
class BaseNode(ABC):
    """
    Abstract class for the nodes
    """

    def __init__(self, config, agent_factory, task_factory):
        self.config = config
        self.agent_factory = agent_factory
        self.task_factory = task_factory

    @abstractmethod
    def execute(self, state):
        pass
