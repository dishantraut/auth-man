
from flask import Blueprint, request, jsonify

from models import UserRoles, User, Role
from database import get_db


user_roles_bp = Blueprint('user_roles', __name__, url_prefix='/iam/user_roles')


@user_roles_bp.route('/', methods=['GET', 'POST'])
def user_roles():
    with next(get_db()) as db:

        if request.method == 'POST':

            data = request.get_json()
            user = db.query(User).filter_by(id=data['user_id']).first()
            if not user:
                return jsonify({"error": "User does not exist"}), 404

            role = db.query(Role).filter_by(id=data['role_id']).first()
            if not role:
                return jsonify({"error": "Role does not exist"}), 404

            existing_user_role = db.query(UserRoles).filter_by(
                user_id=data['user_id'], role_id=data['role_id']).first()

            if existing_user_role:
                return jsonify({"error": "User role already exists"}), 400

            new_user_role = UserRoles(
                user_id=data['user_id'],
                role_id=data['role_id']
            )

            db.add(new_user_role)
            db.commit()

            return jsonify({
                "user_id": new_user_role.user_id,
                "role_id": new_user_role.role_id
            }), 201

        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)

        user_roles = db.query(UserRoles).offset(skip).limit(limit).all()
        return jsonify([{
            "user_id": user_role.user_id,
            "role_id": user_role.role_id
        } for user_role in user_roles])


@user_roles_bp.route('/<int:user_id>/<int:role_id>/', methods=['GET', 'PUT', 'DELETE'])
def user_role_detail(user_id, role_id):
    with next(get_db()) as db:
        user_role = db.query(UserRoles).filter_by(
            user_id=user_id, role_id=role_id).first()

        if not user_role:
            return jsonify({"error": "User role not found"}), 404

        if request.method == 'GET':
            return jsonify({
                "user_id": user_role.user_id,
                "role_id": user_role.role_id
            })

        elif request.method == 'PUT':

            data = request.get_json()
            new_user_id = data.get('user_id', user_id)
            new_role_id = data.get('role_id', role_id)

            user = db.query(User).filter_by(id=new_user_id).first()
            if not user:
                return jsonify({"error": "User does not exist"}), 404

            role = db.query(Role).filter_by(id=new_role_id).first()
            if not role:
                return jsonify({"error": "Role does not exist"}), 404

            existing_user_role = db.query(UserRoles).filter(
                UserRoles.user_id == new_user_id,
                UserRoles.role_id == new_role_id).first()
            if existing_user_role and existing_user_role != user_role:
                return jsonify({"error": "User role combination already exists"}), 400

            user_role.user_id = new_user_id
            user_role.role_id = new_role_id

            db.commit()

            return jsonify({
                "user_id": user_role.user_id,
                "role_id": user_role.role_id
            })

        elif request.method == 'DELETE':
            db.delete(user_role)
            db.commit()
            return jsonify({"message": "User role deleted successfully"}), 204
