#!/usr/bin/python3
"""defines the blueprint for group"""
from flask import Blueprint

group_bp = Blueprint('group', __name__)

from . import group_view
