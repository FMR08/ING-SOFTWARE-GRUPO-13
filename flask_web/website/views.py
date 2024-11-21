from flask import Blueprint, render_template, request, jsonify
from flask_web.website import database as db
from flask_web.website import utils

views = Blueprint('views', __name__)
@views.route('/obtenerCitasDia')
def obtener_citas_dia():
    fecha = request.args.get('fecha')
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT * FROM citas WHERE fecha = %s AND estado != 'cancelada'", (fecha,))
    citas = cursor.fetchall()
    cursor.close()

    # Modificar nombres de columnas según la estructura de la tabla
    for cita in citas:
        cita['paciente'] = db.buscar_paciente(cita['paciente_rut']).nombre

    return jsonify({"citas": citas})



@views.route('/obtenerEspecialistas')
def obtener_especialistas():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT rut,nombre,especialidad,dia,horario_inicio,horario_fin FROM medico")
    results = cursor.fetchall()
    especialistas = [
        {
            "rut": row["rut"],
            "nombre": row["nombre"],
            "especialidad": row["especialidad"],
            "dia": row["dia"],
            "horario": f"{row['horario_inicio']} - {row['horario_fin']}"

        }
        for row in results
    ]

    return jsonify(especialistas)

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
    if not utils.run_valido(run):
        return jsonify({"message": "run invalido", "idCita": id, "status":"error"})
    #revisar si paciente existe en la db
    if db.buscar_paciente(run) is None:
        db.insertar_paciente(run,nombre,apellidos,correo,"555555555")
    #TODO: obtener run del especialista
    run_especialista = 333333333
    #TODO: asegurarse que la id no este repetida en la db, si no, re-generarla

    db.insertar_cita(id,especialista,run,hora,fecha,motivo)


    # Respond back to the frontend
    return jsonify({"message": "Cita registrada con éxito!", "idCita": id, "status":"ok"})

@views.route('/cancelarCita', methods=['POST'])
def cancelar_cita():
    cita_id = request.args.get('id')
    motivo = request.args.get('motivo')

    if not cita_id or not motivo:
        return jsonify({'success': False, 'message': 'Faltan parámetros.'})

    # Llamamos a la función de cancelar la cita
    if db.cancelar_cita(cita_id, motivo):
        return jsonify({'success': True, 'message': 'Cita cancelada correctamente.'})
    else:
        return jsonify({'success': False, 'message': 'Error al cancelar la cita.'})


@views.route('/specialist')
def especialistas():
    return render_template("especialistas.html")

@views.route('/specialist-list')
def lista_especialistas():
    return render_template("lista_especialistas.html")

@views.route('/schedule')
def horario():
    return render_template("horario.html")
