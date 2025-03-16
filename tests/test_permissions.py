import pytest
from flask import Flask
from flask.testing import FlaskClient
from models import Permission
from database import get_db

@pytest.fixture
def client():
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.register_blueprint(per_bp)
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_create_permission(client: FlaskClient):
    response = client.post('/iam/permissions/', json=[
        {'method': 'GET', 'endpoint': '/test'}
    ])
    assert response.status_code == 201
    assert response.json['message'] == 'Permissions created successfully'

def test_get_permissions(client: FlaskClient):
    db = next(get_db())
    permission = Permission(method='GET', endpoint='/test')
    db.add(permission)
    db.commit()

    response = client.get('/iam/permissions/')
    assert response.status_code == 200
    assert len(response.json['permissions']) > 0
