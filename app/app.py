"""
Application entry point
"""

import toml
from flask import Flask

config = toml.load("config.toml")

app = Flask(__name__)
app.config["SECRET_KEY"] = config["app"]["secret_key"]
# app.config["SQLALCHEMY_DATABASE_URI"] = config["app"]["database_url"]
app.config["DEBUG"] = config["app"]["debug"]


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
