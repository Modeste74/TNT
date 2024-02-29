#!/usr/bin/python3
"""defines a class Hub"""
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base

class Hub(BaseModel, Base):
    """Represents the hubs."""
    __tablename__ = 'hubs'

    tutor_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    participants = Column(Integer, default=1)

    tutor = relationship("User", foreign_keys=[tutor_id])
    resources = relationship("Resource", back_populates="hub")
    chats = relationship("Chat", back_populates="hub")
    group = relationship("Group", back_populates="hub")
