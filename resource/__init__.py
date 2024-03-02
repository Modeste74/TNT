#!/usr/bin/python3
"""defines the resource blueprint"""
from flask import Blueprint

resource_bp = Blueprint('resource', __name__)

from . import resource_view
