import os
from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from plugins import db
from site_models import User, Method, Employee, Conference, Publications


basic = Blueprint('main', __name__, url_prefix='')


@basic.route('/')
def home_page():
    data_conferences = db.session.query(Conference).all()

    index_img_path = './static/img/index/'
    index_images = [f"{index_img_path}{img}" for img in os.listdir(index_img_path)]

    return render_template("index.html", title="ЛУМРС", data_conferences=data_conferences, index_images=index_images)


@basic.route('/employees')
def peoples():
    data_employees = {'professor': [], 'work_horse': [], 'student': []}
    data = db.session.query(Employee).all()

    for employee in data:
        data_employees[employee.label].append(employee)

    return render_template("employees.html", title="Состав лаборатории", data_employees=data_employees)


@basic.route('/publications')
def publications():
    data_publications = {}
    data = db.session.query(Publications).all()

    publications_num = len(data)

    for publication in data:
        if publication.year not in data_publications:
            data_publications[publication.year] = []
        data_publications[publication.year].append(publication)

    return render_template("publications.html", title="Публикации", data_publications=data_publications,
                           publications_num=publications_num)


@basic.route('/research')
def research():
    return render_template("research.html", title="Направления исследований")


@basic.route('/methods')
def methods():
    data = db.session.query(Method).all()
    return render_template("methods.html", title="Методы исследований", data_methods=data)


@basic.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Контакты")


@basic.route('/research-materials')
def gallery():
    return render_template("research_materials.html", title="Материалы")


@basic.route('/history')
def history():
    return render_template("history.html", title="История лаборатории")


@basic.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return jsonify('success')
    return jsonify('No-data')


@basic.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home_page'))