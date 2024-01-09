from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager


db = SQLAlchemy()
admin = Admin()
login_manager = LoginManager()
