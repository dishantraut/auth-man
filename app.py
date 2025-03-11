"""
Application entry point
"""

import toml
from flask import Flask, render_template, request, jsonify
from sqlalchemy.orm import joinedload
from werkzeug.security import generate_password_hash

from models import *
from database import get_db


config = toml.load("config.toml")


app = Flask(__name__)
# App configuration
app.config["DEBUG"] = config["app"]["debug"]
app.config["SECRET_KEY"] = config["app"]["secret_key"]
# Database configuration
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = config["database"]["uri"]


@app.route("/")
def hello():

    db = next(get_db())
    users = db.query(User).all()
    roles = db.query(Role).all()
    permissions = db.query(Permission).all()
    user_roles = (
        db.query(UserRoles)
        .options(joinedload(UserRoles.user), joinedload(UserRoles.role))
        .all()
    )
    roles_permissions = (
        db.query(RolePermissions)
        .options(joinedload(RolePermissions.role), joinedload(RolePermissions.permission))
        .all()
    )
    groups = db.query(Group).all()
    # * uncomment for debugging
    # print("\nUsers:", [u.id for u in users])
    # print("\nRoles:", [r.id for r in roles])
    # print("\nPermissions:", [p.id for p in permissions])
    # print("\nUser Roles:", [(ur.user_id, ur.role_id) for ur in user_roles])
    # print("\nRole Permissions:", [(rp.role_id, rp.permission_id) for rp in roles_permissions])
    db.close()

    return render_template(
        "home.html",
        users=users,
        roles=roles,
        groups=groups,
        permissions=permissions,
        user_roles=user_roles,
        roles_permissions=roles_permissions
    )


# # User CRUD operations
# @app.route('/users', methods=['GET', 'POST'])
# def users():
#     db = next(get_db())
#     if request.method == 'POST':
#         data = request.json
#         user = User(
#             username=data['username'],
#             email=data['email'],
#             password=generate_password_hash(data['password'])
#         )
#         db.add(user)
#         db.commit()
#         return jsonify({'message': 'User created successfully'})
#     users = db.query(User).all()
#     return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in users])


# @app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
# def user(id):
#     db = next(get_db())
#     user = db.query(User).get_or_404(id)
#     if request.method == 'DELETE':
#         db.delete(user)
#         db.commit()
#         return jsonify({'message': 'User deleted successfully'})
#     elif request.method == 'PUT':
#         data = request.json
#         user.username = data.get('username', user.username)
#         user.email = data.get('email', user.email)
#         if 'password' in data:
#             user.password = generate_password_hash(data['password'])
#         db.commit()
#         return jsonify({'message': 'User updated successfully'})
#     return jsonify({'id': user.id, 'username': user.username, 'email': user.email})


# @app.route('/roles', methods=['GET', 'POST'])
# def roles():
#     db = next(get_db())
#     if request.method == 'POST':
#         data = request.json
#         role = Role(name=data['name'], description=data.get('description'))
#         db.add(role)
#         db.commit()
#         return jsonify({'message': 'Role created successfully'})
#     roles = db.query(Role).all()
#     return jsonify([{'id': r.id, 'name': r.name, 'description': r.description} for r in roles])


# @app.route('/permissions', methods=['GET', 'POST'])
# def permissions():
#     db = next(get_db())
#     if request.method == 'POST':
#         data = request.json
#         permission = Permission(
#             method=data['method'],
#             endpoint=data['endpoint'],
#             access=data.get('access', False)
#         )
#         db.add(permission)
#         db.commit()
#         return jsonify({'message': 'Permission created successfully'})
#     permissions = db.query(Permission).all()
#     return jsonify([{
#         'id': p.id,
#         'method': p.method,
#         'endpoint': p.endpoint,
#         'access': p.access
#     } for p in permissions])


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
