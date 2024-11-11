#Archivo para añadir datos a la base de datos
from website import create_app, db
from website.models import Paciente, Medico, Cita

app = create_app()

with app.app_context():
    # Agregar un nuevo paciente
    nuevo_paciente = Paciente(nombre='Juan Pérez', fecha_nacimiento='1980-05-15', telefono='555-1234')
    db.session.add(nuevo_paciente)

    # Agregar un nuevo médico
    nuevo_medico = Medico(nombre='Dr. Gómez', especialidad='Cardiología', telefono='555-5678')
    db.session.add(nuevo_medico)

    # Agregar una nueva cita
    nueva_cita = Cita(paciente_id=1, medico_id=1, fecha_hora='2023-10-01 10:00:00', motivo='Chequeo general')
    db.session.add(nueva_cita)

    db.session.commit()  # Guardar los cambios en la base de datos