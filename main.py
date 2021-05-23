from flask import Flask, render_template, redirect
import json


app = Flask(__name__)


@app.route('/')
def home_page():
    with open('conferences.json', 'r', encoding='utf-8') as file:
        data_conferences = json.load(file)
    return render_template("index.html", title="ЛУМРС", conferences=data_conferences)


@app.route('/peoples')
def peoples():
    with open('peoples.json', 'r', encoding='utf-8') as file:
        data_peoples = json.load(file)
    return render_template("peoples.html", title="Состав кафедры", data_peoples=data_peoples)


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


if __name__ == '__main__':
    app.run(debug=True)
