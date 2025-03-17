"""
utils.py - Utility functions for the application
"""

from faker import Faker
from werkzeug.security import generate_password_hash

from models import *
from database import get_db


fake = Faker()


def load_fake_data(num_records=10):
    """
    Load fake data into all models

    Args:
        num_records (int, optional): Number of records to create for each model. Defaults to 10.
    """

    # * Truncate tables first
    db = next(get_db())
    db.query(User).delete()
    db.query(Role).delete()
    db.query(Group).delete()
    db.query(Permission).delete()
    db.query(UserRoles).delete()
    db.query(RolePermissions).delete()
    db.commit()
    db.close()

    # * Create Users
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=generate_password_hash('root', method='pbkdf2:sha256'),
        )
        db = next(get_db())
        db.add(user)
        db.commit()
        db.close()

    # * Create Roles
    roles = [
        Role(name="LocationAdmin", description="Location Supervisor"),
        Role(name="RegionAdmin", description="Region Manager"),
    ]
    db = next(get_db())
    db.bulk_save_objects(roles)
    db.commit()
    db.close()

    # * Create Permissions
    methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    endpoints = ('/billing', '/iam', '/devices', '/config')
    for endpoint in endpoints:
        for method in methods:
            permission = Permission(
                endpoint=endpoint,
                method=method
            )
            db = next(get_db())
            db.add(permission)
            db.commit()
            db.close()

    # * Create UserRoles
    db = next(get_db())
    users = db.query(User).all()
    roles = db.query(Role).all()
    user_role1 = UserRoles(user_id=users[0].id, role_id=roles[0].id)
    user_role2 = UserRoles(user_id=users[0].id, role_id=roles[1].id)
    user_role3 = UserRoles(user_id=users[1].id, role_id=roles[0].id)

    db.add_all([user_role1, user_role2, user_role3])
    db.commit()
    db.close()

    # * Create RolePermissions
    db = next(get_db())
    roles = db.query(Role).all()
    permissions = db.query(Permission).all()

    for role in roles:
        for permission in permissions:
            role_permission = RolePermissions(
                role_id=role.id,
                permission_id=permission.id,
                access=fake.boolean()
            )
            # print(f"Role ID: {role.id}, Permission ID: {permission.id}, Access: {role_permission.access}")
            db.add(role_permission)

    db.commit()
    db.close()

    # * Create Groups
    groups = [
        Group(name="Accounting", description="Accounting Department"),
        Group(name="IT", description="IT Department"),
        Group(name="HR", description="Human Resources")
    ]
    db = next(get_db())
    db.bulk_save_objects(groups)
    db.commit()
    db.close()

    print(f"Created {num_records} fake records for each model")


if __name__ == "__main__":
    load_fake_data()
