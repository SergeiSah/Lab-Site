import json
import os

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, LoginManager, current_user, login_user, logout_user
from werkzeug.security import check_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # секретный ключ для хэширования данных сессии

db = SQLAlchemy(app)
login_manager = LoginManager(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)


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


admin = Admin(app, index_view=MyAdminIndexView())
admin.add_link(LogoutMenuLink(name='Logout', category='', url="/logout"))
admin.add_view(AdminModelView(Conference, db.session))
admin.add_view(EmployeeView(Employee, db.session))


@app.route('/')
def home_page():
    with open('conferences.json', 'r', encoding='utf-8') as file:
        data_conferences = json.load(file)
    return render_template("index.html", title="ЛУМРС", conferences=data_conferences)


@app.route('/employees')
def peoples():
    with open('employees.json', 'r', encoding='utf-8') as file:
        data_peoples = json.load(file)
    return render_template("employees.html", title="Состав лаборатории", data_peoples=data_peoples)


@app.route('/research')
def research():
    return render_template("research.html", title="Направления исследований")


@app.route('/methods')
def methods():
    return render_template("methods.html", title="Методы исследований")


@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Контакты")


@app.route('/gallery')
def gallery():
    return render_template("gallery.html", title="Галерея")


@app.route('/history')
def history():
    return render_template("history.html", title="История лаборатории")


@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return jsonify('success')
    return jsonify('No-data')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))


if __name__ == '__main__':
    app.run(debug=True)
