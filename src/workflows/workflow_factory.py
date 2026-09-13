"""
Contains the factory class for the workflows
"""

import os
from contextlib import suppress

from src.nodes.node_factory import NodeFactory
from src.workflows.components.conditional import ConditionalWorkflow
from src.workflows.components.linear import LinearWorkflow
from src.workflows.components.parallel import ParallelWorkflow

WORKFLOW_TYPES = {
    "linear": LinearWorkflow,
    "parallel": ParallelWorkflow,
    "conditional": ConditionalWorkflow,
}


class WorkflowFactory:
    """
    Creates the workflows based on the configuration
    """

    def __init__(self, config: dict, node_factory: NodeFactory):
        self.config = config
        self.node_factory = node_factory

    def build(self, name: str):
        """Build (but do not compile) the workflow named in the configuration."""
        workflow_config = self.config.get(name)
        if not workflow_config:
            raise ValueError(f"Workflow {name} not found in configuration.")
        workflow_type = workflow_config.get("workflow_type")
        cls = WORKFLOW_TYPES.get(workflow_type)
        if cls is None:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
        workflow = cls(workflow_config, self.node_factory)
        workflow.build_graph()
        workflow.set_entry_and_finish(
            entry_point=workflow_config["entry_point"],
            finish_point=workflow_config["finish_point"],
        )
        return workflow

    def create_workflow(self, name: str):
        """
        Creates and compiles the workflow based on the configuration
        Args:
            name: unique name of the workflow
        Returns:
            compiled LangGraph workflow
        """
        compiled_workflow = self.build(name).compile()
        self.__save_graph_image(compiled_workflow)
        return compiled_workflow

    def create_dynamic_workflow(self):
        return self.create_workflow("dynamic_workflow")

    @staticmethod
    def __save_graph_image(workflow):
        """
        Saves a PNG of the compiled graph when WORKFLOW_GRAPH_IMAGE is set to a path.
        """
        path = os.getenv("WORKFLOW_GRAPH_IMAGE")
        if not path:
            return
        with suppress(Exception):
            img = workflow.get_graph().draw_mermaid_png()
            with open(path, "wb") as f:
                f.write(img)
