"""
Contains the factory class for the workflows
"""

from contextlib import suppress
import json

from src.nodes.node_factory import NodeFactory
from src.workflows.components.conditional import ConditionalWorkflow
from src.workflows.components.linear import LinearWorkflow
from src.workflows.components.parallel import ParallelWorkflow


class WorkflowFactory:
    """
    Creates the workflows based on the configuration
    """

    def __init__(self, config: dict, node_factory: NodeFactory):
        self.config = config
        self.node_factory = node_factory

    def create_workflow(self, name: str):
        """
        Creates the workflow based on the configuration
        Args:
            name: unique name of the workflow

        Returns:

        """
        workflow_config = self.config.get(name)
        workflow_type = workflow_config.get("workflow_type")

        if workflow_type == "linear":
            workflow = LinearWorkflow(workflow_config, self.node_factory)
        elif workflow_type == "parallel":
            workflow = ParallelWorkflow(workflow_config, self.node_factory)
        elif workflow_type == "conditional":
            workflow = ConditionalWorkflow(workflow_config, self.node_factory)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")

        # Build graph, set entry and finish points, and compile the workflow
        workflow.build_graph()
        workflow.set_entry_and_finish(
            entry_point=workflow_config["entry_point"],
            finish_point=workflow_config["finish_point"],
        )
        compiled_workflow = workflow.compile()
        self.__save_graph_image(compiled_workflow)
        return compiled_workflow

    def create_dynamic_workflow(self):
        """
        Creates the workflow based on the configuration

        Returns:

        """
        workflow_config = self.config.get("dynamic_workflow")
        workflow_type = workflow_config.get("workflow_type")

        if workflow_type == "linear":
            workflow = LinearWorkflow(workflow_config, self.node_factory)
        elif workflow_type == "parallel":
            workflow = ParallelWorkflow(workflow_config, self.node_factory)
        elif workflow_type == "conditional":
            workflow = ConditionalWorkflow(workflow_config, self.node_factory)
        else:
            raise ValueError(f"Unknown workflow type: {workflow_type}")

        # Build graph, set entry and finish points, and compile the workflow
        workflow.build_graph()
        workflow.set_entry_and_finish(
            entry_point=workflow_config["entry_point"],
            finish_point=workflow_config["finish_point"],
        )
        compiled_workflow = workflow.compile()
        self.__save_graph_image(compiled_workflow)
        return compiled_workflow

    @staticmethod
    def __save_graph_image(workflow):
        """
        Saves the current created graph workflow image
        Args:
            workflow: compiled workflow

        Returns: NA

        """
        with suppress(Exception):
            img = workflow.get_graph().draw_mermaid_png()
            with open("output_test_image.png", "wb") as f:
                f.write(img)
