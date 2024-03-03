#!/usr/bin/python3
"""Defines a class Resource"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Resource(BaseModel, Base):
    """Representing learning resources"""
    __tablename__ = 'resources'

    hub_id = Column(String(60), ForeignKey('hubs.id'), nullable=False)
    content = Column(String(1024), nullable=False)

    hub = relationship("Hub", back_populates="resources")
