#!/usr/bin/python3
"""defines a blueprint"""
from flask import Blueprint

hub_bp = Blueprint('hub', __name__)

from . import hub_view
