#!/usr/bin/env python3
""" Flask app with user authentication"""
from flask import Flask, jsonify, abort, redirect
from auth import Auth


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> str:
    """ Welcome message """
    message: str = "Bienvenue"
    return jsonify({"message": message})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
