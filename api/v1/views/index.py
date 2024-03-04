#!/usr/bin/python3
"""Create index API"""
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """method that returns the status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def number_of_objects():
    """method return number of objects in all classes"""
    classes = {"amenities": Amenity, "cities": City,
               "places": Place, "reviews": Review,
               "states": State, "users": User}
    newdict = {}
    for key, value in classes.items():
        newdict[key] = storage.count(value)
    return jsonify(newdict)
