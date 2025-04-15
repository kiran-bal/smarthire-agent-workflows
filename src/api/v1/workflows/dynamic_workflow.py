from flask import Blueprint, request, Response, stream_with_context

from src.services.v1.workflows.dynamic_workflow_service import DynamicWorkflowService


url_prefix = '/dynamic'
dynamic_workflow_api = Blueprint("dynamic_workflow_api", __name__, url_prefix=url_prefix)


@dynamic_workflow_api.post("")
def execute_dynamic_workflow():
    """
    API method to invoke the dynamic workflow generation
    """
    stream = request.json.get("stream", "false").lower() == "true"
    workflow_service = DynamicWorkflowService()

    if stream:
        return Response(
            stream_with_context(workflow_service.execute(request=request, stream=True)),
            content_type='text/event-stream'
        )
    else:
        response = workflow_service.execute(request=request, stream=False)
        return response
