#!/usr/bin/python3
"""defines the blueprint for message"""
from flask import Blueprint

message_bp = Blueprint('message', __name__)

from . import message_view
