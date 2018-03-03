#coding: utf-8
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"version":"8.0.0"})

if __name__ == "__main__":
    app.run(host="0.0.0.0")
