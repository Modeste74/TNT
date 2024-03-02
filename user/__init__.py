#!/usr/bin/python3
"""defines users blueprint"""
from flask import Blueprint
from flask_login import LoginManager


user_bp = Blueprint('user', __name__)

login_manager = LoginManager()

from . import user_view
