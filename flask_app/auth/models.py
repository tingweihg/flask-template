from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from flask import current_app

from flask_app.extensions.database import db
from flask_app.extensions.auth import jwt
from flask_app.utils.models import BaseModel


class User(BaseModel):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key = True, nullable=False)
    user_name: Mapped[str] = mapped_column(unique = True, index = True, nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    create_time: Mapped[str] = mapped_column(default = datetime.now(timezone.utc).isoformat(), nullable=False)
    update_time: Mapped[str] = mapped_column(default = datetime.now(timezone.utc).isoformat(), 
                                             onupdate=datetime.now(timezone.utc).isoformat(), 
                                             nullable=False)

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return 'id={}, user_name={}'.format(
            self.id, self.user_name
        )
    
    @staticmethod
    def add_user(user_name, password) -> bool:
        if user_name == "" or password == "":
            current_app.logger.warning('User({}) add failed, {}.'.format(user_name, 'user_name or password is empty.'))
            return False
        user = User.get_by_username(user_name)
        if user is not None:
            current_app.logger.warning('User({}) add failed, {}.'.format(user_name, 'user already exists.'))
            return False
        user = User(user_name, password)
        try:
            db.session.add(user)
            db.session.commit()
            current_app.logger.info('User({}) added.'.format(user_name))
            return True
        except Exception as e:
            current_app.logger.warning('User({}) add failed, {}.'.format(user_name, e))
            db.session.rollback()
            return False

    
    @staticmethod
    def get_by_username(user_name):
        return db.session.query(User).filter(
            User.user_name == user_name
        ).first()
    
    @staticmethod
    def get_by_id(user_id):
        return db.session.query(User).filter(
            User.id == user_id
        ).first()

    @staticmethod
    def get_user_list():
        return db.session.query(User).all()
    
    # @jwt.user_identity_loader
    # def user_identity_lookup(user_name):
    #     user = User.get_by_username(user_name)
    #     return user.id
    
    # @jwt.user_lookup_loader
    # def user_lookup_callback(_jwt_header, jwt_data):
    #     identity = jwt_data["sub"]
    #     return User.query.filter_by(id=identity)
    
    def set_password(self, password) -> None: 
        self.password_hash = generate_password_hash(password)
        self.update_time = datetime.now(timezone.utc).isoformat()
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def identity_name(self):
        return self.user_name
    
    def to_json(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    