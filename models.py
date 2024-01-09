from flask_login import UserMixin, current_user
from flask_admin import AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from plugins import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.id}>"

    def __str__(self):
        return self.name


class Conference(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    dates = db.Column(db.String, nullable=True)

    def __repr__(self):
        return f"<conferences {self.id}>"

    def __str__(self):
        return self.title


class Employee (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    degree = db.Column(db.String, nullable=True)
    position = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    rg = db.Column(db.String, nullable=True)
    sc = db.Column(db.String, nullable=True)
    publons = db.Column(db.String, nullable=True)
    orcid = db.Column(db.String, nullable=True)
    phone = db.Column(db.String, nullable=True)
    email = db.Column(db.String(50), nullable=True)

    def __repr__(self):
        return f"<employees {self.id}>"

    def __str__(self):
        return self.name


class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated


class EmployeeView(AdminModelView):
    form_choices = {
        'label': [
            ('working_horse', 'Рабочая лошадка'),
            ('student', 'Студент'),
            ('professor', 'Профессор')
        ],
    }


class LogoutMenuLink(MenuLink):
    def is_accessible(self):
        return current_user.is_authenticated
