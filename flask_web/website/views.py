from flask import Blueprint, render_template, request, jsonify
from flask_web.website.database import *
from flask_web.website.utils import *
views = Blueprint('views', __name__)
@views.route('/obtenerCitasDia')
def obtener_citas_dia():
    fecha = request.args.get('fecha')
    cursor = database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM citas WHERE fecha = %s", (fecha,))
    citas = cursor.fetchall()
    cursor.close()

    # Modificar nombres de columnas según la estructura de la tabla
    for cita in citas:
        cita['paciente'] = buscar_paciente(cita['paciente_rut']).nombre

    return jsonify({"citas": citas})




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
    correo = data.get('correo')
    fecha = data.get('fecha')
    hora = data.get('hora')
    motivo = data.get('motivo')
    especialista = data.get('specialist')
    id = data.get('idCita')

    run = data.get('rut')
    run = run.replace(".", "").replace("-", "")
    if not run_valido(run):
        return jsonify({"message": "run invalido", "idCita": id, "status":"error"})
    #revisar si paciente existe en la db
    if buscar_paciente(run) is None:
        insertar_paciente(run,nombre,apellidos,correo,"555555555")
    #TODO: obtener run del especialista
    run_especialista = 333333333
    #TODO: asegurarse que la id no este repetida en la db, si no, re-generarla

    insertar_cita(id,run_especialista,run,hora,fecha,motivo)


    # Respond back to the frontend
    return jsonify({"message": "Cita registrada con éxito!", "idCita": id, "status":"ok"})


@views.route('/specialist')
def especialistas():
    return render_template("especialistas.html")

@views.route('/specialist-list')
def lista_especialistas():
    return render_template("lista_especialistas.html")

@views.route('/schedule')
def horario():
    return render_template("horario.html")