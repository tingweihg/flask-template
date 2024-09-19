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
    user_role_id: Mapped[int] = mapped_column(Integer, db.ForeignKey('user_role.id'), nullable=False)

    def __init__(self, user_name, password, role):
        self.user_name = user_name
        self.password_hash = generate_password_hash(password)
        
        from flask_app.auth.models.role import UserRole
        self.user_role_id = UserRole.get_by_name(role).id   

    def __repr__(self):
        return 'id={}, user_name={}, role={}'.format(
            self.id, self.user_name, self.role.role_name
        )
    
    @staticmethod
    def update_user(user_name, password, role) -> bool:
        user = User.get_by_user_name(user_name)
        if user == None:
            current_app.logger.warning('User({}) update failed, {}.'.format(user_name, 'user not exists.')) 
            return False
        if password is not None:
            user.set_password(password)
        from flask_app.auth.models.role import UserRole
        if role in UserRole.choices():
            user.user_role_id = UserRole.get_by_name(role).id
        user.update_time = datetime.now(timezone.utc).isoformat()
        # user.add_to_db()
        db.session.commit()
        current_app.logger.info('User({}) updated.'.format(user_name))
        return True
    
    @staticmethod
    def add_user(user_name, password, role) -> bool:

        # check user_name and password
        if user_name == "" or password == "":
            current_app.logger.warning('User({}) add failed, {}.'.format(user_name, 'user_name or password is empty.'))
            return False
        user = User.get_by_user_name(user_name)

        # check if user exists
        if user is not None:
            current_app.logger.warning('User({}) add failed, {}.'.format(user_name, 'user already exists.'))
            return False
        user = User(user_name, password, role)

        # check role
        from flask_app.auth.models.role import UserRole
        choices = UserRole.choices()
        if role not in choices:
            current_app.logger.warning('User({}) add failed, {}.'.format(user_name, 'role not exists.'))
            return False

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
    def get_by_user_name(user_name):
        return db.session.query(User).filter(
            User.user_name == user_name
        ).first()
    
    @staticmethod
    def get_by_id(user_id):
        return db.session.query(User).filter(
            User.id == user_id
        ).first()

    @staticmethod
    def get_by_role(role_name):  
        all_users = db.session.query(User).all()
        return [user for user in all_users if user.role.role_name == role_name]

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
    