
import pytest

from flask import Flask
from flask.testing import FlaskClient
from werkzeug.security import generate_password_hash

from models import User
from database import get_db
from routes.auth import auth_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(auth_bp)
    with app.test_client() as client:
        with app.app_context():
            yield client


def test_login(client: FlaskClient):
    db = next(get_db())
    password = 'testpassword'
    hashed_password = generate_password_hash(password)
    user = User(username='testuser', email='testuser@example.com',
                password=hashed_password)
    db.add(user)
    db.commit()

    response = client.post('/iam/auth/login/', json={
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': password
    })
    assert response.status_code == 200
    assert response.json['message'] == 'Login successful'


def test_logout(client: FlaskClient):
    response = client.post('/iam/auth/logout/')
    assert response.status_code == 200
    assert response.json['message'] == 'Logged out successfully'
