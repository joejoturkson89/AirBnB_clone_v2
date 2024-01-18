#!/usr/bin/python3
from models.place import Place
from models import storage

# Create the 'places' table
Place.__table__.create(bind=storage._DBStorage__engine, checkfirst=True)

print("Table 'places' created successfully.")
