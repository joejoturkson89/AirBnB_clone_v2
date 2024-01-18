#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy.sql.schema import Table
import models
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
import os

STORAGE = os.getenv("HBNB_TYPE_STORAGE")


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60), ForeignKey('places.id'),
                             primary_key=True, nullable=False),
                      Column('amenity_id', String(60),
                             ForeignKey(
                                 'amenities.id'
                      ), primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship('Review', backref='place',
                           cascade='all, delete, delete-orphan')
    amenities = relationship(
        'Amenity', secondary='place_amenity', viewonly=False, overlaps="place_amenities")

    # For FileStorage
    @property
    def amenity_ids(self):
        return [amenity.id for amenity in self.amenities]

    @amenity_ids.setter
    def amenity_ids(self, amenity_obj):
        if isinstance(amenity_obj, Amenity):
            self.amenities.append(amenity_obj)
