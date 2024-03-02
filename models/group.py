#!/usr/bin/python3
"""defines a class Group"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Group(BaseModel, Base):
    """Represents a group discussion group in a hub"""
    __tablename__ = 'groups'

    hub_id = Column(String(60), ForeignKey('hubs.id'), nullable=False)
    name = Column(String(128), nullable=False)

    hub = relationship("Hub", back_populates="groups")
    members = relationship("GroupMember", back_populates="group")
    messages = relationship("GroupMessage", back_populates="group")


class GroupMessage(BaseModel, Base):
    """Represents a message in a group chat"""
    __tablename__ = 'group_messages'

    group_id = Column(String(60), ForeignKey('groups.id'), nullable=False)
    sender_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    content = Column(String(1024), nullable=False)
    
    group = relationship("Group", back_populates="messages")
    sender = relationship("Users", foreign_keys=[sender_id])
