#!/usr/bin/python3
"""defines the chat blueprint"""
from flask import Blueprint

chat_bp = Blueprint('chat', __name__)

from . import chat_view
