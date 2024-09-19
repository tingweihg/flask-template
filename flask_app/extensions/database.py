from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()



def init_user_role(app):

    from flask_app.auth.models.role import UserRole
    roles = UserRole.get_roles()
    if len(roles) == 0:
        try:
            UserRole.add_role("user", "User")
            UserRole.add_role("moderator", "Moderator")
            UserRole.add_role("admin", "Administrator")
            app.logger.info("User role initialized.")
        except Exception as e:
            app.logger.warning("User role initialized failed, {}.".format(e))


def init_default_users(app):
    from flask_app.auth.models.user import User
    twh_user = User.get_by_user_name("twh")
    if twh_user == None:
        User.add_user("twh", "19921120", "admin")