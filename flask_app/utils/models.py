from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from flask_app.extensions.database import db

# sql base model
class BaseModel(db.Model):
    __abstract__ = True

    # 物件名稱，如使用者的名字等
    def identity_name(self):
        raise NotImplementedError("Please implement this method.")  

    def add_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
            current_app.logger.info('{} ({}) added.'.format(self.__class__.__name__, self.identity_name()))
        except Exception as e:
            current_app.logger.warning('{} ({}) add failed, {}.'.format(self.__class__.__name__, self.identity_name(), e))
            db.session.rollback()

    def delete_to_db(self):
        try:
            db.session.delete(self)
            db.session.commit()
            current_app.logger.info('{} ({}) deleted.'.format(self.__class__.__name__, self.identity_name()))
        except Exception as e:
            current_app.logger.warning('{} ({}) delete failed, {}.'.format(self.__class__.__name__, self.identity_name(), e))
            db.session.rollback()
    
    def to_json(self):
        raise NotImplementedError("Please implement this method.")