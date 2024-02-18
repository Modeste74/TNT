#!/usr/bin/python3
"""defines the storage system for the website"""
from models.engine.db_storage import DBStorage


storage = DBStorage()
storage.reload()