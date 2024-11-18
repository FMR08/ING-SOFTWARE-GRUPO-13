from flask import Blueprint, render_template, request, jsonify
from flask_web.database import *

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html")

@views.route('/book')
def reservas():
    return render_template("reservas.html")

@views.route('/subirReserva', methods=['POST'])
def submit_form():
    data = request.get_json()  # Parse the JSON data sent by JavaScript
    print(f"Received data: {data}")

    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    fecha = data.get('fecha')
    hora = data.get('hora')
    motivo = data.get('motivo')
    especialista = data.get('specialist')
    id = data.get('idCita')
    #TODO: revisar si es un paciente existente (si no, añadirlo a la db)
    #TODO: obtener run del paciente
    run = 222232222
    #TODO: obtener run del especialista
    run_especialista = 333333333
    #TODO: asegurarse que la id no este repetida en la db, si no, re-generarla
    insertar_cita(id,run_especialista,run,hora,fecha,motivo)


    # Respond back to the frontend
    return jsonify({"message": "Cita registrada con éxito!", "idCita": id})


@views.route('/specialist')
def especialistas():
    return render_template("especialistas.html")

@views.route('/specialist-list')
def lista_especialistas():
    return render_template("lista_especialistas.html")

@views.route('/schedule')
def horario():
    return render_template("horario.html")