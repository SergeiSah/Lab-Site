from flask import render_template, redirect, url_for, request, jsonify, Blueprint
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

import config
from plugins import db
from site_models import User, Method, Employee, Conference, Publications
from xray_models import Element, Compound
from forms import OptConstForm


main_bp = Blueprint('main', __name__, url_prefix='')


@main_bp.route('/')
def home_page():
    data_conferences = db.session.query(Conference).all()
    return render_template("index.html", title="ЛУМРС", data_conferences=data_conferences)


@main_bp.route('/employees')
def peoples():
    data_employees = {'professor': [], 'work_horse': [], 'student': []}
    data = db.session.query(Employee).all()

    for employee in data:
        data_employees[employee.label].append(employee)

    return render_template("employees.html", title="Состав лаборатории", data_employees=data_employees)


@main_bp.route('/publications')
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


@main_bp.route('/research')
def research():
    return render_template("research.html", title="Направления исследований")


@main_bp.route('/methods')
def methods():
    data = db.session.query(Method).all()
    return render_template("methods.html", title="Методы исследований", data_methods=data)


@main_bp.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Контакты")


@main_bp.route('/research-materials')
def gallery():
    return render_template("research_materials.html", title="Материалы")


@main_bp.route('/history')
def history():
    return render_template("history.html", title="История лаборатории")


@main_bp.route('/beta-delta', methods=["POST", "GET"])
def beta_delta():
    if request.method == 'POST':
        return

    # download all available elements and compounds from the databases
    choices_el = [(e.Element, e.Element) for e in Element.query.all()]
    choices_comp = [(c.formula, c.formula) for c in Compound.query.all()]

    opt_const_form = OptConstForm()
    opt_const_form.materials.choices = choices_el + choices_comp

    return render_template("beta_delta.html", title="Оптические константы", opt_const_form=opt_const_form)


@main_bp.route('/login', methods=["POST", "GET"])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user and check_password_hash(user.password, request.form['password']):
            login_user(user)
            return jsonify('success')
    return jsonify('No-data')


@main_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_page'))