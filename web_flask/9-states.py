#!/usr/bin/python3
"""Importing Flask."""
from flask import Flask, render_template
from models import storage
from models.state import State


app = Flask(__name__)


@app.teardown_appcontext
def teardown(self):
    """Method to remove current session"""
    storage.close()


@app.route('/states', strict_slashes=False)
def states():
    """Displays a html page with states."""
    states = storage.all(State)
    return render_template('9-states.html', states=states, mode='all')



@app.route('/states/<id>', strict_slashes=False)
def state_by_id(id):
    """display a html page with cities of the state."""
    for state in storage.all(State).values():
        if state.id == id:
            return render_template('9-states.html', states=states, mode='id')
    return render_template('9-states.html', states=states, mode='none')


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
