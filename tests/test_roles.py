import pytest
from flask import json
from app import create_app
from database import get_db
from models import Role

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            # Initialize the database
            db = next(get_db())
            db.execute('PRAGMA foreign_keys = ON')
            db.commit()
        yield client

def test_get_roles(client):
    response = client.get('/iam/roles/')
    assert response.status_code == 200

def test_create_role(client):
    new_role = {'roles': [{'name': 'admin', 'description': 'Administrator role'}]}
    response = client.post('/iam/roles/', data=json.dumps(new_role), content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data[0]['name'] == 'admin'
    assert data[0]['description'] == 'Administrator role'

def test_create_existing_role(client):
    new_role = {'roles': [{'name': 'admin', 'description': 'Administrator role'}]}
    client.post('/iam/roles/', data=json.dumps(new_role), content_type='application/json')
    response = client.post('/iam/roles/', data=json.dumps(new_role), content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert "Role 'admin' already exists." in data['errors']

def test_get_role(client):
    new_role = {'roles': [{'name': 'admin', 'description': 'Administrator role'}]}
    client.post('/iam/roles/', data=json.dumps(new_role), content_type='application/json')
    response = client.get('/iam/roles/1/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'admin'
    assert data['description'] == 'Administrator role'

def test_update_role(client):
    new_role = {'roles': [{'name': 'admin', 'description': 'Administrator role'}]}
    client.post('/iam/roles/', data=json.dumps(new_role), content_type='application/json')
    updated_role = {'name': 'superadmin', 'description': 'Super Administrator role'}
    response = client.put('/iam/roles/1/', data=json.dumps(updated_role), content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['name'] == 'superadmin'
    assert data['description'] == 'Super Administrator role'

def test_delete_role(client):
    new_role = {'roles': [{'name': 'admin', 'description': 'Administrator role'}]}
    client.post('/iam/roles/', data=json.dumps(new_role), content_type='application/json')
    response = client.delete('/iam/roles/1/')
    assert response.status_code == 204
    response = client.get('/iam/roles/1/')
    assert response.status_code == 404
