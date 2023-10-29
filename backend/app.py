from flask import Flask, jsonify, session, abort, redirect, request
import os
import pathlib
from model.vectorprompt import find_nearest_lawyers


app = Flask("flask analytix")

@app.route('/')
def home():
    return ''

@app.route("/api/prompt", methods=["POST"])
def prompt_api():
    # Get the input string from the POST request
    input_string = request.json.get("input_string")
    if input_string is not None:
        with app.app_context():
            # Inside the application context, call your model function
            result =find_nearest_lawyers('backend/model/PS_2_Test_Dataset.csv', input_string, n_neighbors=5)
        return jsonify({"result": result})
    else:
        return jsonify({"error": "Input string not provided in the request."}), 400

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
