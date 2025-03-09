from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(200))


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    method = Column(String)
    endpoint = Column(String)
    access = Column(Boolean, default=False)


# class UserRole(Base):
#     __tablename__ = 'user_roles'

#     user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
#     role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())


# class RolePermission(Base):
#     __tablename__ = 'role_permissions'

#     role_id = Column(Integer, ForeignKey('roles.id'), primary_key=True)
#     permission_id = Column(Integer, ForeignKey(
#         'permissions.id'), primary_key=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())


if __name__ == "__main__":
    from database import engine
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
