
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from models import User
from database import get_db

# TODO : add jwt token based access
# TODO : rate limit login attempts
# TODO : re-captcha google

auth_bp = Blueprint('auth', __name__, url_prefix='/iam/auth')


@auth_bp.route('/login/', methods=['POST'])
def login():
    """ Handle user login """

    try:
        db = next(get_db())
        data = request.get_json()

        if not all(key in data for key in ['username', 'email', 'password']):
            return jsonify({'error': 'Missing username or password'}), 400

        user = db.query(User).filter_by(username=data['username']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({'error': 'Invalid username or password'}), 401

        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }), 200

    except Exception as e:
        return jsonify({'error': 'Server error'}), 500

    finally:
        db.close()


@auth_bp.route('/logout/', methods=['POST'])
def logout():
    """ Handle user logout """
    try:
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500
