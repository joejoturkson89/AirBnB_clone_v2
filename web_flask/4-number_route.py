#!/usr/bin/python3
"""This script starts a flask web application.
The web application must be listening on 0.0.0.0, port 5000
"""

from flask import Flask

app = Flask("__name__")


@app.route('/', strict_slashes=False)
def hello():
    """Return a given string."""
    return ("Hello HBNB!")


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    """Return a given string."""
    return ("HBNB")


@app.route("/c/<text>", strict_slashes=False)
def cText(text):
    """Display C followed by the text variable value."""
    return "C {}".format(text.replace("_", " "))


@app.route('/python', strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def pythonText(text="is cool"):
    """Display python then value of text variable."""
    return "Python {}".format(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def isNumber(n):
    """Display 'n is a nuber' only if n is an integer"""
    if isinstance(n, int):
        return "{} is a number".format(n)



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=None)
