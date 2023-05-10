from flask import Flask, jsonify, Response
""" Flask app"""

app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def welcome() -> Response:
    """ Welcome message """
    message: str = "Bienvenue"
    return jsonify({"message": message}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
