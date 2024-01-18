#!/usr/bin/python3
"""This is the file storage class for AirBnB"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """This class serializes instances to a JSON file and
    deserializes JSON file to instances
    Attributes:
        __file_path: path to the JSON file
        __objects: objects will be stored
    """
    __file_path = "file.json"
    __objects = {}
    all_classes = {'BaseModel': BaseModel, 'User': User,
                   'State': State, 'City': City, 'Amenity': Amenity,
                   'Place': Place, 'Review': Review}

    def all(self, cls=None):
        """returns a dictionary
        Return:
            returns a dictionary of __object
        """
        all_return = {}

        # if cls is valid
        if cls:
            if cls.__name__ in self.all_classes:
                # copy objects of cls to temp dict
                for key, val in self.__objects.items():
                    if key.split('.')[0] == cls.__name__:
                        all_return.update({key: val})
        else:  # if cls is none
            all_return = self.__objects

        return all_return

    def new(self, obj):
        """sets __object to given obj
        Args:
            obj: given object
        """
        if obj:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj

    def save(self):
        """serialize the file path to JSON file path
        """
        my_dict = {}
        for key, value in self.__objects.items():
            my_dict[key] = value.to_dict()
        with open(self.__file_path, 'w', encoding="UTF-8") as f:
            json.dump(my_dict, f)

    def reload(self):
        """serialize the file path to JSON file path
        """
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, value in (json.load(f)).items():
                    value = eval(value["__class__"])(**value)
                    self.__objects[key] = value
        except FileNotFoundError:
            pass

    def close(self):
        """Reload JSON objects
        """
        return self.reload()

    def delete(self, obj=None):
        """delete obj from __objects if present
        """
        if obj:
            # format key from obj
            key = "{}.{}".format(type(obj).__name__, obj.id)
            del self.__objects[key]
# """This module defines a class to manage file storage for hbnb clone"""
# import json


# class FileStorage:
#     """This class manages storage of hbnb models in JSON format"""
#     __file_path = 'file.json'
#     __objects = {}

#     def all(self, cls=None):
#         """Returns a dictionary or a filtered dictionary of models"""
#         if cls is None:
#             return FileStorage.__objects
#         return {
#             k: v for k, v in FileStorage.__objects.items()
#             if isinstance(v, cls)
#             }

#     def new(self, obj):
#         """Adds new object to storage dictionary"""
#         self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

#     def save(self):
#         """Saves storage dictionary to file"""
#         with open(FileStorage.__file_path, 'w') as f:
#             temp = {}
#             temp.update(FileStorage.__objects)
#             for key, val in temp.items():
#                 temp[key] = val.to_dict()
#             json.dump(temp, f)

#     def reload(self):
#         """Loads storage dictionary from file"""
#         from models.base_model import BaseModel
#         from models.user import User
#         from models.place import Place
#         from models.state import State
#         from models.city import City
#         from models.amenity import Amenity
#         from models.review import Review

#         classes = {
#                     'BaseModel': BaseModel, 'User': User, 'Place': Place,
#                     'State': State, 'City': City, 'Amenity': Amenity,
#                     'Review': Review
#                   }
#         try:
#             temp = {}
#             with open(FileStorage.__file_path, 'r') as f:
#                 temp = json.load(f)
#                 for key, val in temp.items():
#                     self.all()[key] = classes[val['__class__']](**val)
#         except FileNotFoundError:
#             pass

#     def delete(self, obj=None):
#         """Deletes obj from __objects if it's inside"""
#         if obj is not None:
#             key = obj.__class__.__name__ + '.' + obj.id
#             if key in FileStorage.__objects:
#                 del FileStorage.__objects[key]
