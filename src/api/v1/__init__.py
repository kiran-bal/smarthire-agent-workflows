from flask import Blueprint

from src.api.v1.workflows import workflows_apis


url_prefix = '/v1'
v1_apis = Blueprint('v1_api', __name__, url_prefix=url_prefix)

@v1_apis.get("/ping")
def ping():
    """Test Ping
    """
    return "ping success!!"


# Static workflow APIs
v1_apis.register_blueprint(workflows_apis)

