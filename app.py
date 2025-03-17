"""
Application entry point
"""

import toml
from flask import Flask, render_template


from models import *
from database import get_db
from routes.auth import auth_bp
from routes.users import users_bp
from routes.permissions import per_bp
from routes.roles import roles_bp
from routes.groups import groups_bp
from routes.user_roles import user_roles_bp
from routes.role_permissions import role_permissions_bp


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
app.register_blueprint(groups_bp)
app.register_blueprint(user_roles_bp)
app.register_blueprint(role_permissions_bp)



@app.route("/")
def hello():
    """
    Render the home page with users, roles, permissions, groups and their relationships.

    Returns:
        str: Rendered HTML template with database query results
    """
    with next(get_db()) as db:
        users = db.query(User).all()
        roles = db.query(Role).all()
        permissions = db.query(Permission).all()
        groups = db.query(Group).all()

        user_roles = (
            db.query(UserRoles, User, Role)
            .join(User, UserRoles.user_id == User.id)
            .join(Role, UserRoles.role_id == Role.id)
            .all()
        )

        # ! Uncomment For Debugging
        # print("\nUser Roles:")
        # print("User ID\tUsername\tRole ID\tRole Name")
        # print("-" * 50)
        # for user_role, user, role in user_roles:
        #     print(f"{user.id}\t{user.username}\t{role.id}\t{role.name}")

        roles_permissions = (
            db.query(RolePermissions, Role, Permission)
            .join(Role, RolePermissions.role_id == Role.id)
            .join(Permission, RolePermissions.permission_id == Permission.id)
            .all()
        )

        # ! Uncomment For Debugging
        # print("\nRoles Permissions:")
        # print("Role ID\tRole Name\tRole Description\tPermission ID\tMethod\tEndpoint\tAccess")
        # print("-" * 100)
        # for role_perm, role, permission in roles_permissions:
        #     print(f"{role.id}\t{role.name}\t{role.description}\t{permission.id}\t{permission.method}\t{permission.endpoint}\t{role_perm.access}")

    return render_template(
        "home.html",
        users=users,
        roles=roles,
        groups=groups,
        permissions=permissions,
        user_roles=user_roles,
        roles_permissions=roles_permissions
    )


if __name__ == "__main__":
    app.run(
        port=8000,
        debug=True,
        threaded=True,
        host="0.0.0.0",
        use_reloader=True,
        use_debugger=True
    )
