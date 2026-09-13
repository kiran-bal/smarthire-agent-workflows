import os
import secrets

from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from src.api import api_urls


load_dotenv()


def create_app():
    """Flask App"""
    app = Flask(__name__, static_url_path="")
    # Set FLASK_SECRET_KEY in the environment; the random fallback is for local runs only.
    app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

    CORS(app)

    app.register_blueprint(api_urls)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)
