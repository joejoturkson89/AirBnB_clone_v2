#!/usr/bin/python3
"""This module initializes the storage engine."""
from os import getenv
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

storage.reload()

# """This module instantiates an object of class FileStorage or DBStorage"""
# import os
# from models.engine.file_storage import FileStorage
# from models.engine.db_storage import DBStorage
# from sqlalchemy.orm import registry

# mapper_registry = registry()


# if os.getenv('HBNB_TYPE_STORAGE') == 'db':
#     storage = DBStorage()
# else:
#     storage = FileStorage()

# storage.reload()
