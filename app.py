"""
Application entry point
"""

import toml
from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash, check_password_hash

from models import *
from database import get_db
from routes.auth import auth_bp
from routes.users import users_bp
from routes.permissions import per_bp
from routes.roles import roles_bp


config = toml.load("config.toml")


app = Flask(__name__)
# * App configuration
app.config["DEBUG"] = config["app"]["debug"]
app.config["SECRET_KEY"] = config["app"]["secret_key"]
# * Database configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = config["database"]["uri"]



# * Register blueprints
app.register_blueprint(per_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(users_bp)
app.register_blueprint(roles_bp)


@app.route("/")
def hello():

    db = next(get_db())
    users = db.query(User).all()
    roles = db.query(Role).all()
    permissions = db.query(Permission).all()
    # user_roles = db.query(UserRoles).all()

    user_roles = (
        db.query(UserRoles)
        .options(joinedload(UserRoles.user), joinedload(UserRoles.role))
        .all()
    )

    # roles_permissions = (
    #     db.query(RolePermissions)
    #     .options(joinedload(RolePermissions.role), joinedload(RolePermissions.permission))
    #     .all()
    # )
    # groups = db.query(Group).all()

    # print("\nUser Roles:", [(ur.user_id, ur.role_id) for ur in user_roles])
    # print("\nRole Permissions:", [(rp.role_id, rp.permission_id) for rp in roles_permissions])
    db.close()

    return render_template(
        "home.html",
        users=users,
        roles=roles,
        groups=None,
        permissions=permissions,
        user_roles=user_roles,
        roles_permissions=None
    )








# @app.route('/groups', methods=['GET', 'POST'])
# def groups():
#     db = next(get_db())
#     if request.method == 'POST':
#         data = request.json
#         group = Group(name=data['name'], description=data.get('description'))
#         db.add(group)
#         db.commit()
#         return jsonify({'message': 'Group created successfully'})
#     groups = db.query(Group).all()
#     return jsonify([{'id': g.id, 'name': g.name, 'description': g.description} for g in groups])


if __name__ == "__main__":
    app.run(
        port=8000,
        debug=True,
        threaded=True,
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True
    )

