#!/usr/bin/python3
""" Amenity Module for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel):
    """ Amenity class to store amenity information """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False, unique=True)
    place_amenities = relationship('PlaceAmenity', backref='amenity',
                                   cascade='all, delete, delete-orphan')
