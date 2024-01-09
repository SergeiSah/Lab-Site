import json

from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from plugins import admin, login_manager
from config import Config
from models import *


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY'] = Config.SECRET_KEY  # секретный ключ для хэширования данных сессии

db.init_app(app)
admin.init_app(app)
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


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
