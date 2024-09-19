from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from flask import current_app

from flask_app.extensions.database import db
from flask_app.extensions.auth import jwt
from flask_app.utils.models import BaseModel
from flask_app.auth.models.user import User


class UserRole(BaseModel):
    __tablename__ = "user_role"
    
    id: Mapped[int] = mapped_column(primary_key = True, nullable=False)
    role_name: Mapped[str] = mapped_column(unique = True, index = True, nullable=False)
    description: Mapped[str] = mapped_column(unique = True, index = True, nullable=False)
    users = relationship("User", backref="role")

    def __init__(self, name, description):
        self.role_name = name
        self.description = description

    def __repr__(self):
        return 'id={}, name={}'.format(
            self.id, self.role_name
        )
    
    def identity_name(self):
        return self.role_name
    
    def to_json(self):
        return {
            'id': self.id,
            'role_name': self.role_name,
            'description': self.description
        }
    
    @staticmethod
    def choices():
        roles = db.session.query(UserRole).all()
        return [role.role_name for role in roles]

    @staticmethod
    def get_by_name(name):
        return db.session.query(UserRole).filter(
            UserRole.role_name == name
        ).first()
    
    @staticmethod
    def get_roles():
        return db.session.query(UserRole).all()
    
    @staticmethod
    def get_role_by_name(name):
        return db.session.query(UserRole).filter(
            UserRole.role_name == name
        ).first()
    
    @staticmethod
    def get_role_by_id(role_id):
        return db.session.query(UserRole).filter(
            UserRole.id == role_id
        ).first()
    
    @staticmethod
    def get_role_users_by_id(role_id: int):
        return db.session.query(User).filter(
            User.user_role_id == role_id
        ).all()
    
    def add_role(name, description) -> bool:
        if name == "":
            current_app.logger.warning('Role({}) add failed, {}.'.format(name, 'name is empty.'))
            return False
        role = UserRole.get_by_name(name)
        if role is not None:
            current_app.logger.warning('Role({}) add failed, {}.'.format(name, 'role already exists.'))
            return False
        role = UserRole(name, description)
        try:
            db.session.add(role)
            db.session.commit()
            current_app.logger.info('Role({}) added.'.format(name))
            return True
        except Exception as e:
            current_app.logger.warning('Role({}) add failed, {}.'.format(name, e))
            db.session.rollback()
            return False
        
    