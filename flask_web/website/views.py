from flask import Blueprint, request, jsonify, render_template
from .models import Paciente, Medico, Cita, db

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/medicos', methods=['GET'])
def listar_medicos():
    medicos = Medico.query.all()
    return render_template('medicos.html', medicos=medicos)

@views.route('/horarios', methods=['GET'])
def ver_horarios():
    medicos = Medico.query.all()
    horarios_disponibles = {}
    
    for medico in medicos:
        citas = Cita.query.filter_by(medico_id=medico.id).all()
        horarios_disponibles[medico.nombre] = [cita.fecha_hora for cita in citas]
    
    return render_template('horarios.html', horarios=horarios_disponibles)