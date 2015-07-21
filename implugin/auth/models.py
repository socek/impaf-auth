from hashlib import sha1
import os

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

from .model_base import DeclarativeBase
from .db_tables import users_2_permissions


class BasePermission(AbstractConcreteBase, DeclarativeBase):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    group = Column(String)

    def __repr__(self):
        data = self.__class__.__name__
        name = self.name or ''
        group = self.group or ''
        return '%s: %s:%s' % (data, name, group)

    def to_str(self):
        name = self.name or ''
        group = self.group or ''
        return '%s:%s' % (group, name)


class BaseUser(object):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String(128))

    @declared_attr
    def permissions(cls):
        return relationship(
            cls._permission_cls,
            secondary=users_2_permissions,
        )

    def has_permission(self, group, name):
        for permission in self.permissions:
            if permission.name == name and permission.group == group:
                return True
        return False

    def has_access_to_route(self, route):
        ctrl = self.registry['route'].routes[route]
        return self.has_access_to_controller(ctrl)

    def has_access_to_controller(self, ctrl):
        permissions = getattr(ctrl, 'permissions', [])
        for group, name in permissions:
            if not self.has_permission(group, name):
                return False
        return True

    def set_password(self, password):
        hashed_password = password

        salt = sha1()
        salt.update(os.urandom(60))
        hash = sha1()
        hash.update((password + salt.hexdigest()).encode('utf8'))
        hashed_password = salt.hexdigest() + hash.hexdigest()

        self.password = hashed_password

    def validate_password(self, password):
        hashed_pass = sha1()
        hashed_pass.update((password + self.password[:40]).encode('utf8'))
        return self.password[40:] == hashed_pass.hexdigest()

    def is_authenticated(self):
        return True

    def __repr__(self):
        data = self.__class__.__name__
        name = self.name or ''
        email = self.email or ''
        return '%s: %s (%s)' % (data, name, email)


class NotLoggedUser(BaseUser):
    id = None
    name = 'not logged user'
    email = None
    password = None
    permissions = []

    def has_permission(self, group, name):
        return False

    def set_password(self, *args, **kwargs):
        raise NotImplementedError()

    def validate_password(self, *args, **kwargs):
        raise NotImplementedError()

    def is_authenticated(self):
        return False

    def has_access_to_controller(self, ctrl):
        return getattr(ctrl, 'permissions', []) == []


class Permission(BasePermission):
    pass


class User(BaseUser, DeclarativeBase):
    __tablename__ = 'users'
    _permission_cls = Permission
