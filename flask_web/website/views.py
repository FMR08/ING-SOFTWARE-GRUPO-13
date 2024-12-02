from flask import Blueprint, render_template, request, jsonify
from flask_web.website import database as db
from flask_web.website import utils
import re

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


#Se ha añadido precio_consulta
@views.route('/obtenerEspecialistas')
def obtener_especialistas():
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("SELECT rut,nombre,especialidad,dia,horario_inicio,horario_fin, precio_consulta FROM medico")
    results = cursor.fetchall()
    especialistas = [
        {
            "rut": row["rut"],
            "nombre": row["nombre"],
            "especialidad": row["especialidad"],
            "dia": row["dia"],
            "horario": f"{row['horario_inicio']} - {row['horario_fin']}",
            "Precio de consulta": row["precio_consulta"]

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
    
def correo_valido(correo):
    # Expresión regular para validar correos electrónicos
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, correo) is not None
    
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
    # Validar correo
    if not correo_valido(correo):
        return jsonify({"message": "Correo inválido", "idCita": id, "status": "error"})
    #revisar si paciente existe en la db
    if db.buscar_paciente(run) is None:
        db.insertar_paciente(run,nombre,apellidos,correo,"555555555")
    #TODO: obtener run del especialista
    run_especialista = 333333333
    #TODO: asegurarse que la id no este repetida en la db, si no, re-generarla

    db.insertar_cita(id,especialista,run,hora,fecha,motivo,"Confirmada")


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

@views.route('/registrarUsuario', methods=['POST'])
def registrar_usuario():
    try:
        # Obtener y validar los datos de la solicitud
        data = request.get_json()
        if not data:
            return jsonify({"message": "Solicitud JSON inválida"}), 400

        # Extraer datos
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        correo = data.get('correo')
        telefono = data.get('telefono')
        contraseña = data.get('contraseña')
        rut = data.get('rut')
        
        if not all([nombre, apellidos, correo, telefono, contraseña, rut]):
            return jsonify({"message": "Todos los campos son obligatorios"}), 400

        # Validar RUT
        rut = rut.replace(".", "").replace("-", "")
        print("n: "+nombre+ " a: "+apellidos+" c: "+correo+" t: " +telefono+" c: "+
              contraseña+" r: "+rut)
        if db.buscar_usuarios(rut):
            return jsonify({"message": "El usuario ya está registrado"}), 409
        db.insertar_usuarios(rut, nombre, apellidos, correo, telefono, contraseña)
        return jsonify({"message": "¡Usuario registrado con éxito!"}), 201

    except Exception as e:
        # Loggear el error en la consola para depuración
        print(f"Error interno del servidor: {e}")
        return jsonify({"message": "Ocurrió un error interno", "error": str(e)}), 500

@views.route('/resumen/<id_cita>')
def resumen(id_cita):
    cursor = db.database.cursor(dictionary=True)
    cursor.execute("""
        SELECT c.id, c.fecha, c.hora, c.motivo, 
               m.nombre AS especialista, m.precio_consulta 
        FROM citas c 
        JOIN medico m ON c.medico = m.rut 
        WHERE c.id = %s
    """, (id_cita,))
    cita = cursor.fetchone()
    cursor.close()

    if not cita:
        return "Cita no encontrada", 404

    return render_template("resumen.html", cita=cita)


@views.route('/sign-up')
def registrarse():
    return render_template("registrarse.html")

@views.route('/specialist')
def especialistas():
    return render_template("especialistas.html")

@views.route('/specialist-list')
def lista_especialistas():
    return render_template("lista_especialistas.html")

@views.route('/schedule')
def horario():
    return render_template("horario.html")
