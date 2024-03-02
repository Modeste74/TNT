#!/usr/bin/python3
"""defines a class Users"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Enum
from sqlalchemy.orm import relationship
from hashlib import md5
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from models.messages import Message


class Users(UserMixin, BaseModel, Base):
    """defines class and it table"""
    __tablename__ = 'users'
    id = Column(String(60), primary_key=True)
    password = Column(String(500), nullable=False)
    username = Column(String(128), nullable=False, unique=True)
    user_type = Column(Enum('tutor', 'learner'), nullable=False)

    def __init__(self, *args, **kwargs):
    	"""initializes user"""
    	super().__init__(*args, **kwargs)
    	if 'password' in kwargs:
    	    self.set_password(kwargs['password'])

    def set_password(self, password):
    	"""sets the password to hash"""
    	hashed_password = generate_password_hash(password)
    	self.password = hashed_password

    def check_password(self, password):
    	"""Checkes the password"""
    	return check_password_hash(self.password, password)
    
    sent_messages = relationship("Message", foreign_keys=[Message.sender_id], back_populates="sender")
    received_messages = relationship("Message", foreign_keys=[Message.receiver_id], back_populates="receiver")
    hubs = relationship("Hub", secondary="hub_learners", back_populates="learners")
    hubs_association = relationship("HubLearners", back_populates="learner", overlaps="hubs")