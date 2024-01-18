#!/usr/bin/python3
"""This module defines the DBStorage class."""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import os

class DBStorage:
    """This class defines the MySQL storage engine."""
    __engine = None
    __session = None

    def __init__(self):
        """Create the engine, and create all tables if not exists."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(os.getenv('HBNB_MYSQL_USER'),
                                              os.getenv('HBNB_MYSQL_PWD'),
                                              os.getenv('HBNB_MYSQL_HOST'),
                                              os.getenv('HBNB_MYSQL_DB')),
                                      pool_pre_ping=True)
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''query on the current db session all cls objects'''
        dct = {}
        if cls is None:
            for c in classes.values():
                objs = self.__session.query(c).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    dct[key] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                dct[key] = obj
        return dct

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session."""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and create the current session."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))

    def close(self):
        """Close the current session."""
        self.__session.remove()


# """This module defines the DBStorage engine for HBNB"""
# from sqlalchemy import create_engine, MetaData
# from sqlalchemy.orm import sessionmaker, scoped_session
# import os
# from models.base_model import Base
# from models.user import User
# from models.state import State
# from models.city import City
# from models.amenity import Amenity
# from models.place import Place
# from models.review import Review


# class DBStorage:
#     """This class defines the DBStorage engine"""
#     __engine = None
#     __session = None

#     def __init__(self):
#         """Initializes the DBStorage engine"""
#         self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
#                                       .format(os.getenv('HBNB_MYSQL_USER'),
#                                               os.getenv('HBNB_MYSQL_PWD'),
#                                               os.getenv('HBNB_MYSQL_HOST'),
#                                               os.getenv('HBNB_MYSQL_DB')),
#                                       pool_pre_ping=True)
#         if os.getenv('HBNB_ENV') == 'test':
#             Base.metadata.drop_all(self.__engine)

#     def all(self, cls=None):
#         """Queries on the current database session"""
#         classes = [User, State, City, Amenity, Place, Review]

#         if cls:
#             classes = [cls]

#         objects_dict = {}
#         for c in classes:
#             objects = self.__session.query(c).all()
#             for obj in objects:
#                 key = '{}.{}'.format(obj.__class__.__name__, obj.id)
#                 objects_dict[key] = obj

#         return objects_dict

#     def new(self, obj):
#         """Adds the object to the current database session"""
#         self.__session.add(obj)

#     def save(self):
#         """Commits all changes of the current database session"""
#         self.__session.commit()

#     def delete(self, obj=None):
#         """Deletes from the current database session"""
#         if obj:
#             self.__session.delete(obj)

#     def reload(self):
#         """
#         Creates all tables in the database and creates
#         the current database session
#         """
#         Base.metadata.create_all(self.__engine)
#         self.__session = scoped_session(sessionmaker(
#             bind=self.__engine, expire_on_commit=False))

#     def close(self):
#         """Calls remove() on the private session attribute"""
#         self.__session.remove()