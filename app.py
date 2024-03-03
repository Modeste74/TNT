#!/usr/bin/python3
"""defines the app for our web application"""
from flask import Flask
from user import user_bp, login_manager
from message import message_bp
from hub import hub_bp
from resource import resource_bp
from chat import chat_bp
from group import group_bp
import os


def create_app():
    """creates an application and registers the
    necessary blueprint"""
    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_SECRET_KEY')

    app.register_blueprint(user_bp)
    app.register_blueprint(message_bp)
    app.register_blueprint(hub_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(resource_bp)
    app.register_blueprint(group_bp)

    login_manager.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)

