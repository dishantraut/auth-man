"""
Application entry point
"""

import toml
from flask import Flask, render_template
from models import User, Role, Permission

from database import get_db


config = toml.load("config.toml")

app = Flask(__name__)
app.config["DEBUG"] = config["app"]["debug"]
app.config["SECRET_KEY"] = config["app"]["secret_key"]
# Add database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = config["database"]["uri"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


@app.route("/")
def hello():
    db = next(get_db())
    users = db.query(User).all()
    roles = db.query(Role).all()
    permissions = db.query(Permission).all()
    # user_roles = db.query(User.username, Role.name).join(User.roles).all()
    # roles_permissions = db.query(Role.name, Permission.name).join(Role.permissions).all()
    db.close()
    return render_template(
        "home.html",
        users=users,
        roles=roles,
        permissions=permissions,
        # user_roles=user_roles,
        # roles_permissions=roles_permissions
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
