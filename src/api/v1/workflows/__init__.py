from flask import Blueprint

from src.api.v1.workflows.dynamic_workflow import dynamic_workflow_api

url_prefix = '/workflow'
workflows_apis = Blueprint('workflows_apis', __name__, url_prefix=url_prefix)

workflows_apis.register_blueprint(dynamic_workflow_api)

