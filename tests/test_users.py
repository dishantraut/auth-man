
import pytest

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from models import User
from database import get_db
from routes.users import users_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(users_bp)
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_create_user(client: FlaskClient):
    response = client.post('/iam/users/', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'


def test_get_users(client: FlaskClient):
    db = next(get_db())
    password = 'testpassword'
    hashed_password = generate_password_hash(password)
    user = User(username='testuser', email='testuser@example.com',
                password=hashed_password)
    db.add(user)
    db.commit()

    response = client.get('/iam/users/')
    assert response.status_code == 200
    assert len(response.json) > 0


def test_get_user_detail(client: FlaskClient):
    db = next(get_db())
    password = 'testpassword'
    hashed_password = generate_password_hash(password)
    user = User(username='testuser', email='testuser@example.com',
                password=hashed_password)
    db.add(user)
    db.commit()

    response = client.get(f'/iam/users/{user.id}/')
    assert response.status_code == 200
    assert response.json['username'] == 'testuser'
