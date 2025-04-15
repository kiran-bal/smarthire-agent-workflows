from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from src.api import api_urls


load_dotenv()


def create_app():
    """Flask App"""
    app = Flask(__name__, static_url_path="")
    app.secret_key = "667-634-197"

    CORS(app)

    app.register_blueprint(api_urls)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
