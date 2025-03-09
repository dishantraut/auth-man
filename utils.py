from faker import Faker
from models import User, Role, Permission
from database import get_db

# Import your other models here

fake = Faker()

def load_fake_data(num_records=10):
    """
    Load fake data into all models

    Args:
        num_records (int, optional): Number of records to create for each model. Defaults to 10.
    """

    # * Truncate tables first
    db = next(get_db())
    # db.query(UserRole).delete()
    # db.query(RolePermission).delete()
    db.query(User).delete()
    db.query(Role).delete()
    db.query(Permission).delete()
    db.commit()
    db.close()

    # * Create fake users
    for _ in range(5):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password='root',
        )
        db = next(get_db())
        db.add(user)
        db.commit()
        db.close()

    # * Create fake roles
    roles = [
        Role(name="LocationAdmin", description="Location Supervisor"),
        Role(name="RegionAdmin", description="Region Manager"),
    ]
    db = next(get_db())
    db.bulk_save_objects(roles)
    db.commit()
    db.close()

    # * Create fake permissions
    methods = ('GET', 'POST', 'PUT', 'PATCH', 'DELETE')
    endpoints = ('/billing', '/iam', '/devices', '/config')
    for endpoint in endpoints:
        for method in methods:
            permission = Permission(
                endpoint=endpoint,
                method=method,
                access=fake.boolean()
            )
            db = next(get_db())
            db.add(permission)
            db.commit()
            db.close()

    # # Add fake user-role assignments
    # for _ in range(num_records):
    #     user_role = UserRole(
    #         user_id=fake.random_int(min=1, max=num_records),
    #         role_id=fake.random_int(min=1, max=num_records)
    #     )
    #     db = next(get_db())
    #     db.add(user_role)
    #     db.commit()
    #     db.close()

    # # Add fake role-permission assignments
    # for _ in range(num_records):
    #     role_permission = RolePermission(
    #         role_id=fake.random_int(min=1, max=num_records),
    #         permission_id=fake.random_int(min=1, max=num_records)
    #     )
    #     db = next(get_db())
    #     db.add(role_permission)
    #     db.commit()
    #     db.close()

    print(f"Created {num_records} fake records for each model")

if __name__ == "__main__":
    load_fake_data()