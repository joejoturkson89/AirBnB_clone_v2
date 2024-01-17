#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship(
        "City", back_populates="state", cascade="all, delete-orphan")

    @property
    def cities(self):
        """Getter attribute for cities that returns the list of City instances
        with state_id equals to the current State.id
        """
        return [city for city in models.storage.all(
            "City").values() if city.state_id == self.id]
