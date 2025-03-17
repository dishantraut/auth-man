
from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash

from models import User
from database import get_db

# TODO : add jwt token based access >> share the same token into django
# TODO : rate limit login attempts >> leverage redis container
# TODO : re-captcha google
# TODO : document the code via sphinx
# TODO : add logging
# TODO : add user registration
# TODO : add password reset
# TODO : add email verification
# TODO : postman api collection & documentation
# TODO : add tests case for CI/CD run
# TODO : group related requirement pending


auth_bp = Blueprint('auth', __name__, url_prefix='/iam/auth')


@auth_bp.route('/login/', methods=['POST'])
def login():
    """
    Handle user login by validating credentials

    Returns:
        tuple: JSON response with user data and HTTP status code
    """
    with next(get_db()) as db:
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


@auth_bp.route('/logout/', methods=['POST'])
def logout():
    """ Handle user logout """
    try:
        return jsonify({'message': 'Logged out successfully'}), 200
    except Exception as e:
        return jsonify({'error': 'Server error'}), 500
