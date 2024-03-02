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

    tutor = relationship("Users", foreign_keys=[tutor_id])
    resources = relationship("Resource", back_populates="hub")
    chats = relationship("Chat", back_populates="hub")
    groups = relationship("Group", back_populates="hub")
    learners = relationship("Users", secondary="hub_learners", back_populates="hubs", overlaps="hubs_association")
    learners_association = relationship("HubLearners", back_populates="hub", overlaps="hubs,learners")


class HubLearners(BaseModel, Base):
    """defines a class for learners in hubs"""
    __tablename__ = 'hub_learners'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hub_id = Column(String(60), ForeignKey('hubs.id'), nullable=False)
    learner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    hub = relationship("Hub", back_populates="learners_association", overlaps="hubs,learners")
    learner = relationship("Users", back_populates="hubs_association", overlaps="hubs,learners")
