#!/usr/bin/python3
"""defines a class GroupMember"""
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class GroupMember(BaseModel, Base):
    """represents member of a discussion group"""
    __tablename__ = 'group_members'

    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    group_id = Column(String(60), ForeignKey('groups.id'), nullable=False)

    user = relationship("User", foreign_keys=[user_id])
    group = relationship("Group", back_populates="members")
