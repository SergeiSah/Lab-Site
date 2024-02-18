from flask import Flask
from config import Config
from plugins import admin, login_manager
from basic_pages.models import *
from basic_pages.views import basic
from calc_pages.views import calc


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = Config.SECRET_KEY  # секретный ключ для хэширования данных сессии
    app.config['SQLALCHEMY_BINDS'] = Config.SQLALCHEMY_BINDS

    app.register_blueprint(basic)
    app.register_blueprint(calc)

    db.init_app(app)

    admin.init_app(app)
    login_manager.init_app(app)

    admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
    admin.add_view(AdminModelView(Conference, db.session))
    admin.add_view(EmployeeView(Employee, db.session))
    admin.add_view(AdminModelView(Method, db.session))

    return app
