from abc import ABC, abstractmethod

from src.configuration.dynamic_config_manager import DynamicConfigManager


class AbstractWorkflowAdapter(ABC):
    """
    Abstract base class for workflow adapters.
    All workflow adapters must implement these methods.
    """

    def __init__(self):
        # TODO: Remove hardcoded path and implement hierarchy
        self.config_manager = DynamicConfigManager(
            f"src/tools/tools_registry/tools.yaml",
            f"src/agents/agent_registry/agents.yaml",
            f"src/tasks/tasks_registry/tasks.yaml",
            f"src/nodes/nodes_registry/nodes.yaml"
        )

    @abstractmethod
    def adapt_workflow(self, source_config):
        """
        Abstract method to adapt the workflow.
        Must be implemented by all concrete adapters.
        """
        pass

    @abstractmethod
    def validate_request_structure(self):
        """
        Abstract method to validate the request structure.
        Can be customized per adapter type.
        """
        pass