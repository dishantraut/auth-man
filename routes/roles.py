from flask import Blueprint, request, jsonify

from database import get_db
from models import Role, UserRoles

roles_bp = Blueprint('roles', __name__, url_prefix='/iam/roles')


@roles_bp.route('/', methods=['GET', 'POST'])
def get_roles():

    with next(get_db()) as db:

        if request.method == 'POST':
            data = request.get_json()
            roles_data = data.get('roles', [])
            errors, added_roles = [], []
            existing_roles = {role.name for role in db.query(Role).all()}

            for role_data in roles_data:
                if role_data['name'] in existing_roles:
                    errors.append(
                        f"Role '{role_data['name']}' already exists.")
                    continue
                new_role = Role(
                    name=role_data['name'], description=role_data.get('description'))
                db.add(new_role)
                db.commit()
                added_roles.append(new_role)
                existing_roles.add(new_role.name)

            if errors:
                return jsonify({"errors": errors}), 400

            return jsonify([role.to_dict() for role in added_roles]), 201

        roles = db.query(Role).all()
        return jsonify([
            {
                'id': role.id,
                'name': role.name,
                'description': role.description
            } for role in roles
        ])


@roles_bp.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE', 'PATCH'])
def handle_role(id):
    with next(get_db()) as db:
        role = db.query(Role).filter_by(id=id).first()
        if role is None:
            return jsonify({"error": "Role not found"}), 404

        if request.method == 'GET':
            return jsonify(role.to_dict())

        elif request.method == 'PUT':
            data = request.get_json()
            role.name = data['name']
            role.description = data.get('description')
            db.commit()
            return jsonify(role.to_dict())

        elif request.method == 'DELETE':
            db.delete(role)
            db.commit()
            return '', 204

        elif request.method == 'PATCH':
            data = request.get_json()
            if 'name' in data:
                role.name = data['name']
            if 'description' in data:
                role.description = data['description']
            db.commit()
            return jsonify(role.to_dict())
