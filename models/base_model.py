#!/usr/bin/python3
"""Defines a class BaseModel"""
from datetime import datetime
import models
import uuid
from sqlalchemy import Column, DateTime, String
from sqlalchemy.ext.declarative import declarative_base

time = "%Y-%m-%dT%"
Base = declarative_base()


class BaseModel:
    """defines BaselModel"""
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Intialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
            	if key != "__class__":
            	    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
            	self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
            	self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
            	self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
            	self.id = str(uuid.uuid4())
        else:
        	self.id = str(uuid.uuid4())
        	self.created_at = datetime.utcnow()
        	self.updated_at = self.created_at

    def __str__(self):
    	"""string rep of the basemodel class"""
    	return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
    		self.__dict__)

    def save(self):
    	"""updates the attribute 'updated_at'
    	with the current datetime"""
    	self.updated_at = datetime.utcnow()
    	models.storage.new(self)
    	models.storage.save()

    def to_dict(self):
    	"""return a dictionary containing all keys/values of the
    	instance"""
    	new_dict =  self.__dict__.copy()
    	if "created_at" in new_dict:
    		new_dict["created_at"] = new_dict["created_at"].strftime(time)
    	if "updated_at" in new_dict:
    		new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
    	new_dict["__class__"] = self.__class__.__name__
    	if "_sa_instance_state" in new_dict:
    		del new_dict["_sa_instance_state"]
    	return new_dict

    def delete(self):
    	"""deletes the current instance from the stage"""
    	models.storage.delete(self)