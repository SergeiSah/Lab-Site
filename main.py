from flask import render_template, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash

from plugins import login_manager, db
from models import User, Method, Employee, Conference, Publications
from app import create_app
from forms import LoginForm


app = create_app()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.context_processor
def global_variables():
    login_form = LoginForm()
    return dict(login_form=login_form)


@app.route('/')
def home_page():
    data_conferences = db.session.query(Conference).all()
    return render_template("index.html", title="ЛУМРС", data_conferences=data_conferences)


@app.route('/employees')
def peoples():
    data_employees = {'professor': [], 'work_horse': [], 'student': []}
    data = db.session.query(Employee).all()

    for employee in data:
        data_employees[employee.label].append(employee)

    return render_template("employees.html", title="Состав лаборатории", data_employees=data_employees)


@app.route('/publications')
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


@app.route('/research')
def research():
    return render_template("research.html", title="Направления исследований")


@app.route('/methods')
def methods():
    data = db.session.query(Method).all()
    return render_template("methods.html", title="Методы исследований", data_methods=data)


@app.route('/contacts')
def contacts():
    return render_template("contacts.html", title="Контакты")


@app.route('/research-materials')
def gallery():
    return render_template("research_materials.html", title="Материалы")


@app.route('/history')
def history():
    return render_template("history.html", title="История лаборатории")


@app.route('/beta-delta')
def beta_delta():
    return render_template("beta_delta.html", title="Оптические константы")


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
