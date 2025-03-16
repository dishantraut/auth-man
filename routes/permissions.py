
from flask import Blueprint, request, jsonify

from models import Permission
from database import get_db


per_bp = Blueprint('permissions', __name__, url_prefix='/iam/permissions')


@per_bp.route('/', methods=['GET', 'POST'])
def permissions():
    with next(get_db()) as db:

        if request.method == 'POST':
            data = request.json
            endpoint_permissions = {}

            for item in data:
                endpoint = item['endpoint']
                if endpoint not in endpoint_permissions:
                    endpoint_permissions[endpoint] = 0
                endpoint_permissions[endpoint] += 1
                if endpoint_permissions[endpoint] > 5:
                    return jsonify({'message': f'Cannot add more than 5 permissions for endpoint {endpoint}'}), 400

            for item in data:
                endpoint = item['endpoint']
                existing_permissions = db.query(
                    Permission).filter_by(endpoint=endpoint).all()
                if len(existing_permissions) >= 5:
                    return jsonify({'message': f'Cannot add more than 5 permissions for endpoint {endpoint}'}), 400

                allowed_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
                if item['method'] not in allowed_methods:
                    return jsonify({'message': f'Method {item["method"]} is not allowed'}), 400

                methods = [perm.method for perm in existing_permissions]
                if item['method'] in methods:
                    return jsonify({'message': f'Method {item["method"]} already exists for endpoint {endpoint}'}), 400

                permission = Permission(
                    method=item['method'],
                    endpoint=item['endpoint']
                )
                db.add(permission)
            db.commit()
            return jsonify({'message': 'Permissions created successfully'}), 201

        # * GET method
        permissions = db.query(Permission).all()
        return jsonify({'permissions': [{
            'id': p.id,
            'method': p.method,
            'endpoint': p.endpoint
        } for p in permissions]}), 200


@per_bp.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def permission_detail(id):
    with next(get_db()) as db:
        permission = db.query(Permission).get(id)

        if not permission:
            return jsonify({'message': 'Permission not found'}), 404

        if request.method == 'GET':
            return jsonify({
                'id': permission.id,
                'method': permission.method,
                'endpoint': permission.endpoint
            })

        elif request.method == 'DELETE':
            db.delete(permission)
            db.commit()
            return jsonify({'message': 'Permission deleted successfully'})


