#!/usr/bin/python3
"""Importing Flask."""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.route("/hbnb_filters", strict_slashes=False)
def hbnb_filters():
    """Displays the main hbnb filter page."""
    states = storage.all("State")
    amenities = storage.all("Amenity")
    return render_template("10-hbnb_filters.html",
            states=states, amenities=amenities)

@app.teardown_appcontext
def teardown(exc):
    """remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
