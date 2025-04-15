from flask import Blueprint

from src.api.v1 import v1_apis


url_prefix = '/api'
api_urls = Blueprint('api_urls', __name__, url_prefix=url_prefix)

api_urls.register_blueprint(v1_apis)