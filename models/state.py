#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City
import os
import models
# from models import mapper_registry  # Importing mapper_registry from __init__.py
STORAGE = os.getenv("HBNB_TYPE_STORAGE")
# Import the mapper_registry



class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if STORAGE == "db":
        name = Column(String(128), nullable=False)
        cities = relationship(
            'City', back_populates='state', cascade="all, delete-orphan", foreign_keys="[City.state_id]")

    else:
        name = ""


        @property
        def cities(self):
            """Getter attribute for cities that returns the list of City instances
            with state_id equals to the current State.id
            """
            return [city for city in models.storage.all(
                "City").values() if city.state_id == self.id]


