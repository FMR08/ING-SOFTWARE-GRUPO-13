from flask import Blueprint, render_template

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/book')
def reservas():
    return render_template("reservas.html")

@views.route('/specialist')
def especialistas():
    return render_template("especialistas.html")