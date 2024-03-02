#!/usr/bin/python3
"""defines a class Chat"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Chat(BaseModel, Base):
    """Represents a group chat in a hub."""
    __tablename__ = 'chats'

    hub_id = Column(String(60), ForeignKey('hubs.id'), nullable=False)
    sender_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    message = Column(String(1024), nullable=False)

    hub = relationship("Hub", back_populates="chats")
    sender = relationship("Users", foreign_keys=[sender_id])
