from datetime import datetime, timezone
from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
# from flask_jwt_extended 
from flask import current_app

from flask_app.extensions import db, jwt


class User(db.Model):
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

    def __repr__(self) -> str:
        return 'id={}, user_name={}'.format(
            self.id, self.user_name
        )
    
    
    @staticmethod
    def get_by_username(user_name):
        with current_app.app_context():
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
    
    def add_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info('User({}) added.'.format(self.user_name))
        except Exception as e:
            print(f'Error: {e}')
            current_app.logger.warning('User({}) add failed, {}.'.format(self.user_name, e))
            db.session.rollback()

    def delete_from_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('User({}) deleted.'.format(self.user_name))
        except Exception as e:
            print(f'Error: {e}')
            current_app.logger.warning('User({}) delete failed, {}.'.format(self.user_name, e))
            db.session.rollback()
    
    def update(self):
        db.session.commit()
    
    def to_json(self):
        return {
            'id': self.id,
            'user_name': self.user_name,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    