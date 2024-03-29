#!/usr/bin/python3
"""defines a class DBStorage"""
import models
from models.base_model import BaseModel, Base
from models.messages import Message
from models.users import Users
from models.hub import Hub, HubLearners
from models.resource import Resource
from models.chat import Chat
from models.group import Group, GroupMessage
from models.group_members import GroupMember
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from os import getenv

classes = {"Users": Users, "Message": Message, "Hub": Hub,
        "HubLearners": HubLearners, "Resource": Resource,
        "Chat": Chat, "Group": Group, "GroupMember": GroupMember,
        "GroupMessage": GroupMessage, "BaseModel": BaseModel}


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        USER = getenv('TNT_MYSQL_USER')
        PWD = getenv('TNT_MYSQL_PWD')
        HOST = getenv('TNT_MYSQL_HOST')
        DB = getenv('TNT_MYSQL_DB')
        ENV = getenv('TNT_ENV')
        self.__engine = create_engine(
            f'mysql+mysqldb://{USER}:{PWD}@{HOST}/{DB}')
        if ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + str(obj.id)
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes from the current database
        session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """calls remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its
        ID, or None if found
        """
        if cls not in classes.values():
            return None
        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value
        return None

    def count(self, cls=None):
        """
        counts number of object in storage
        """
        all_class = classes.values()
        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())
        return count
