from flask import Flask
from config import Config
from plugins import admin, db, login_manager
from models import *


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = Config.SECRET_KEY  # секретный ключ для хэширования данных сессии

    db.init_app(app)
    admin.init_app(app)
    login_manager.init_app(app)

    admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
    admin.add_view(AdminModelView(Conference, db.session))
    admin.add_view(EmployeeView(Employee, db.session))
    admin.add_view(AdminModelView(Method, db.session))

    return app
