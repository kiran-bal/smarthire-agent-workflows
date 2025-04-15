from src.adapters.generic_adapter import GenericWorkflowAdapter
from src.adapters.custom_conditional_adapter import CustomConditionalAdapter


class WorkflowAdapterFactory:
    """
    Factory class to create workflow adapters.
    """

    def __init__(self):
        pass  # Pass the configuration shared across all adapters

    def get_adapter(self, workflow_source):
        """
        Get the appropriate adapter instance based on the workflow type.
        :param workflow_source: Type of workflow (e.g., "linear", "conditional").
        :return: An instance of a workflow adapter.
        """
        if workflow_source == 'default':
            return GenericWorkflowAdapter()
        if workflow_source == 'custom_conditional':
            return CustomConditionalAdapter()
        # Additional workflow types can be added here in the future
        else:
            raise ValueError(f"Unsupported workflow type: {workflow_source}")
