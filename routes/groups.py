from flask import Blueprint, request, jsonify

from models import Group
from database import get_db


groups_bp = Blueprint('groups', __name__, url_prefix='/iam/groups')


@groups_bp.route('/', methods=['GET', 'POST'])
def groups():
    with next(get_db()) as db:
        if request.method == 'POST':

            data = request.get_json()
            existing_group = db.query(Group).filter_by(
                name=data['name']).first()
            if existing_group:
                return jsonify({"error": "Group with this name already exists"}), 400

            new_group = Group(
                name=data['name'],
                description=data.get('description')
            )

            db.add(new_group)
            db.commit()

            return jsonify({
                "id": new_group.id,
                "name": new_group.name,
                "description": new_group.description
            }), 201

        skip = request.args.get('skip', 0, type=int)
        limit = request.args.get('limit', 100, type=int)

        # SELECT * FROM groups LIMIT {limit} OFFSET {skip}
        groups = db.query(Group).offset(skip).limit(limit).all()
        return jsonify([{
            "id": group.id,
            "name": group.name,
            "description": group.description
        } for group in groups])


@groups_bp.route('/<int:group_id>/', methods=['GET', 'PUT', 'DELETE'])
def group_detail(group_id):

    with next(get_db()) as db:
        group = db.query(Group).get(group_id)

        if not group:
            return jsonify({"error": "Group not found"}), 404

        if request.method == 'GET':
            return jsonify({
                "id": group.id,
                "name": group.name,
                "description": group.description
            })

        elif request.method == 'PUT':
            data = request.get_json()

            if 'name' in data:
                existing_group = db.query(Group).filter(
                    Group.name == data['name']).first()

            if existing_group:
                return jsonify({"error": "Group with this name already exists"}), 400

            group.name = data['name']
            if 'description' in data:
                group.description = data['description']

            db.commit()

            return jsonify({
                "id": group.id,
                "name": group.name,
                "description": group.description
            })

        elif request.method == 'DELETE':
            db.delete(group)
            db.commit()
            return jsonify({"message": "Group deleted successfully"}), 204
