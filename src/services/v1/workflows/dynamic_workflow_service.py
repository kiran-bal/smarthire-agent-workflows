import json
import os
from datetime import datetime

from dotenv import load_dotenv
from flask import Request
import traceback

from constants import CURRENT_DATETIME_KEY
from constants.http_status_codes import HTTP_202_ACCEPTED
from src.adapters.adapter_factory import WorkflowAdapterFactory
from src.managers.templates.template_manager import TemplateManager

from src.workflows.dynamic_workflow_orchestrator import DynamicWorkflowOrchestrator

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


class DynamicWorkflowService:
    """
    Class for dynamic workflow creation
    """

    def __init__(self) -> None:
        self.template_manager = TemplateManager()
        self.workflow_orchestrator = DynamicWorkflowOrchestrator()
        self.adapter_factory = WorkflowAdapterFactory()

    def execute(self, request: Request, stream: bool = False):
        """method to build and run the dynamic workflow
        Args:
            request (Request): request from API
            stream: decides whether to give streaming response or not
        Returns:
            GenericAPIException
        """
        try:
            data = request.json

            payload = data.get("payload", {})

            adapter = self.adapter_factory.get_adapter(workflow_source="default")
            # adapter = self.adapter_factory.get_adapter(workflow_source="custom_conditional")
            new_config = adapter.adapt_workflow(source_config=payload)

            workflow_factory = self.workflow_orchestrator.get_workflow_factory(
                config=new_config
            )

            workflow = workflow_factory.create_workflow(name="dynamic_workflow")

            inputs = {
                "curr_execution_node": None,
                "current_time": self.get_current_time(),
                CURRENT_DATETIME_KEY: self.get_current_time()
            }

            if stream:
                def generate():
                    try:
                        for chunk in workflow.stream(input=inputs, stream_mode="updates"):
                            if isinstance(chunk, (dict, list)):
                                my_data = json.dumps(chunk)
                            else:
                                my_data = str(chunk)
                            # SSE format: data: <data>\n\n
                            yield f"data: {my_data}\n\n"
                            yield ":"
                    except Exception:
                        error_chunk = {
                            "status": HTTP_202_ACCEPTED,
                            "result": {},
                            "error": traceback.format_exc(),
                            "message": "Streaming failed",
                            "is_Success": False
                        }
                        yield f"data: {json.dumps(error_chunk)}\n\n"
                        yield ":"

                return generate()
            else:
                result = workflow.invoke(
                    input=inputs
                )

                return {
                    "status": HTTP_202_ACCEPTED,
                    "message": "Success",
                    "result": result,
                    "error": "",
                    "is_Success": True
                }
        except Exception as ex:
            return {
                "status": HTTP_202_ACCEPTED,
                "result": {},
                "error": traceback.format_exc(),
                "message": "Failed",
                "is_Success": False

            }

    @staticmethod
    def get_current_time():
        return datetime.now().isoformat(timespec='seconds')
