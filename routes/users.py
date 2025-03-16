
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from models import User
from database import get_db


users_bp = Blueprint('users', __name__, url_prefix='/iam/users')


@users_bp.route('/', methods=['GET', 'POST'])
def users():
    """ Handle user creation and listing """
    with next(get_db()) as db:

        if request.method == 'POST':
            data = request.get_json()

            if not all(key in data for key in ['username', 'email', 'password']):
                return jsonify({'error': 'Missing required fields'}), 400

            if db.query(User).filter_by(username=data['username']).first():
                return jsonify({'error': 'Username already exists'}), 409

            if db.query(User).filter_by(email=data['email']).first():
                return jsonify({'error': 'Email already exists'}), 409

            hashed_password = generate_password_hash(
                data['password'], method='pbkdf2:sha256')
            user = User(
                username=data['username'],
                email=data['email'],
                password=hashed_password
            )

            try:
                db.add(user)
                db.commit()
                return jsonify({'message': 'User created successfully'}), 201
            except Exception as e:
                db.rollback()
                return jsonify({'error': 'Database error'}), 500

        # * GET method
        users = db.query(User).all()
        return jsonify([
            {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'password': user.password
            } for user in users
        ])


@users_bp.route('/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def user(id):
    with next(get_db()) as db:
        user = db.query(User).get(id)

        if not user:
            return jsonify({'error': 'User not found'}), 404

        if request.method == 'GET':
            return jsonify({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }), 200

        elif request.method == 'DELETE':
            db.delete(user)
            db.commit()
            return jsonify({'message': 'User deleted successfully'}), 204

        elif request.method == 'PUT':
            data = request.json
            user.username = data.get('username', user.username)
            user.email = data.get('email', user.email)
            if 'password' in data:
                user.password = generate_password_hash(
                    data['password'], method='pbkdf2:sha256')
            db.commit()
            return jsonify({'message': 'User updated successfully'})

        return jsonify({'id': user.id, 'username': user.username, 'email': user.email})
