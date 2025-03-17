from flask import Blueprint, request, jsonify

from models import RolePermissions, Role, Permission
from database import get_db


role_permissions_bp = Blueprint(
    'role_permissions', __name__, url_prefix='/iam/role_permissions')


@role_permissions_bp.route('/', methods=['GET', 'POST'])
def role_permissions():
    with next(get_db()) as db:

        if request.method == 'POST':

            data = request.get_json()
            role = db.query(Role).filter_by(id=data['role_id']).first()
            if not role:
                return jsonify({"error": "Role does not exist"}), 404

            permission = db.query(Permission).filter_by(
                id=data['permission_id']).first()
            if not permission:
                return jsonify({"error": "Permission does not exist"}), 404

            existing_role_permission = db.query(RolePermissions).filter_by(
                role_id=data['role_id'], permission_id=data['permission_id']).first()

            if existing_role_permission:
                return jsonify({"error": "Role permission already exists"}), 400

            new_role_permission = RolePermissions(
                role_id=data['role_id'],
                permission_id=data['permission_id'],
                access=data.get('access', False)
            )

            db.add(new_role_permission)
            db.commit()

            return jsonify({
                "role_id": new_role_permission.role_id,
                "permission_id": new_role_permission.permission_id,
                "access": new_role_permission.access
            }), 201

        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)
        role_permissions = db.query(RolePermissions).offset(skip).limit(limit).all()

        return jsonify([{
            "role_id": role_permission.role_id,
            "permission_id": role_permission.permission_id,
            "access": role_permission.access
        } for role_permission in role_permissions])


@role_permissions_bp.route('/<int:role_id>/<int:permission_id>/', methods=['GET', 'PUT', 'DELETE'])
def role_permission_detail(role_id, permission_id):
    with next(get_db()) as db:
        role_permission = db.query(RolePermissions).filter_by(
            role_id=role_id, permission_id=permission_id).first()

        if not role_permission:
            return jsonify({"error": "Role permission not found"}), 404

        if request.method == 'GET':
            return jsonify({
                "role_id": role_permission.role_id,
                "permission_id": role_permission.permission_id,
                "access": role_permission.access
            })

        elif request.method == 'PUT':

            data = request.get_json()
            new_role_id = data.get('role_id', role_id)
            new_permission_id = data.get('permission_id', permission_id)
            new_access = data.get('access', role_permission.access)

            role = db.query(Role).filter_by(id=new_role_id).first()
            if not role:
                return jsonify({"error": "Role does not exist"}), 404

            permission = db.query(Permission).filter_by(
                id=new_permission_id).first()
            if not permission:
                return jsonify({"error": "Permission does not exist"}), 404

            existing_role_permission = db.query(RolePermissions).filter(
                RolePermissions.role_id == new_role_id,
                RolePermissions.permission_id == new_permission_id).first()
            if existing_role_permission and existing_role_permission != role_permission:
                return jsonify({"error": "Role permission combination already exists"}), 400

            role_permission.role_id = new_role_id
            role_permission.permission_id = new_permission_id
            role_permission.access = new_access

            db.commit()

            return jsonify({
                "role_id": role_permission.role_id,
                "permission_id": role_permission.permission_id,
                "access": role_permission.access
            })

        elif request.method == 'DELETE':
            db.delete(role_permission)
            db.commit()
            return jsonify({"message": "Role permission deleted successfully"}), 204
