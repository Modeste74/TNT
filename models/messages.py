#!/usr/bin/python3
"""defines a class Message"""
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship


class Message(BaseModel, Base):
    """Reps message"""
    __tablename__ = 'messages'
    id = Column(String(128), primary_key=True)
    sender_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    receiver_id = Column(String(128), ForeignKey('users.id'), nullable=False)
    message = Column(String(1024))
    image = Column(LargeBinary)
    video = Column(LargeBinary)

    def __init__(self, *args, **kwargs):
        """initialzes messages"""
        super().__init__(*args, **kwargs)

    sender = relationship("Users", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("Users", foreign_keys=[receiver_id], back_populates="received_messages")
