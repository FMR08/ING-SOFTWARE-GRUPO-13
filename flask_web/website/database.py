import mysql.connector
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import re

database = mysql.connector.connect(
    host='sql10.freemysqlhosting.net',
    user='sql10748269',
    password='EI4pljbcyV',
    database='sql10748269'
)
class Usuarios:
    def __init__(self, rut, nombre,apellido, email, telefono, contraseña):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono
        self.contraseña = contraseña

class Paciente:
    def __init__(self, rut, nombre,apellido, email, telefono):
        self.rut = rut
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.telefono = telefono

class Medico:
    def __init__(self, rut, nombre, correo, contraseña, especialidad,dia,Hora_I,Hora_F,precio_consulta):
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.especialidad = especialidad
        self.dia = dia
        self.horario_inicio = Hora_I
        self.horario_fin = Hora_F
        self.precio_consulta = precio_consulta

class Administrador:
    def __init__(self, rut, nombre, correo, contraseña):
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña

class Citas:
    def __init__(self, id, medico, paciente, hora, fecha, motivo,estado):
        self.id = id
        self.medico = medico
        self.paciente = paciente
        self.hora = hora
        self.fecha = fecha
        self.motivo = motivo
        self.estado = estado

def ver_tablas():
    cursor = database.cursor()
    
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    for table in tables:
        print(f"tabla "+ table[0]+": ")
        cursor.execute(f"SELECT * FROM "+table[0])
        rows = cursor.fetchall()
        for row in rows:
            print(row)
    cursor.close()

    #database.close()

# Función para eliminar la cita y registrar el motivo de la cancelación
def cancelar_cita(id, motivo):
    cursor = database.cursor()
    fecha_cancelacion = datetime.now()
    # Insertar motivo de cancelación en una tabla de "cancelaciones" (suponiendo que ya existe)
    cursor.execute("INSERT INTO cancelaciones (id_cita, motivo, fecha_cancelacion) VALUES (%s, %s, %s)", (id, motivo,fecha_cancelacion))
    
    # Marcar la cita de la tabla de "citas" como cancelada
    cursor.execute("UPDATE citas SET estado='cancelada' WHERE id = %s", (id,))
    
    database.commit()
    cursor.close()
    return True


def atributos():
    cursor = database.cursor()
    cursor.execute("DESCRIBE medico")
    rows = cursor.fetchall()
    print("Atributos de la tabla citas:")
    for row in rows: 
        print(row)

    cursor.close()
    #database.close()

def insertar_usuarios(rut,nombre,apellido,email, telefono, contraseña):
    cursor = database.cursor()
    cursor.execute("INSERT INTO usuarios (rut, nombre, apellido, email, telefono, contraseña) VALUES (%s, %s, %s, %s, %s, %s)",(rut,nombre,apellido,email, telefono,contraseña))
    print("Usuarios "+ nombre+ " insertado")
    database.commit()
    cursor.close()

def insertar_paciente(rut,nombre,apellido,email, telefono):
    cursor = database.cursor()
    cursor.execute("INSERT INTO paciente (rut, nombre, apellido, email, telefono) VALUES (%s, %s, %s, %s, %s)",(rut,nombre,apellido,email, telefono))
    print("Paciente "+ nombre+ " insertado")
    database.commit()
    cursor.close()

def insertar_administrador(rut, nombre, correo, contraseña):
    cursor = database.cursor()
    cursor.execute("INSERT INTO administrador (rut, nombre, correo, contraseña) VALUES (%s, %s, %s, %s)", (rut, nombre, correo, contraseña))
    print("Administrador "+ nombre+ " insertado")
    database.commit()
    cursor.close()
    #database.close()

def insertar_medico(rut, nombre, correo, contraseña, especialidad, dia, horario_inicio, horario_fin, precio_consulta):
    cursor = database.cursor()
    cursor.execute("INSERT INTO medico (rut, nombre, email, contraseña, especialidad, dia, horario_inicio, horario_fin, precio_consulta) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",(rut, nombre, correo, contraseña, especialidad, dia, horario_inicio, horario_fin, precio_consulta))
    print("Medico "+ nombre+ " insertado")
    database.commit()
    cursor.close()
    #database.close()

def insertar_cita(id, run_medico, run_paciente, hora, fecha, motivo,estado):
    cursor = database.cursor()
    cursor.execute("INSERT INTO citas (id, medico, paciente, hora, fecha, motivo, estado) VALUES (%s, %s, %s, %s, %s, %s, %s)", (id, run_medico, run_paciente, hora, fecha, motivo, estado))
    database.commit()
    #print("Cita "+ id + " insertada")
    paciente =buscar_paciente(run_paciente)
    medico = buscar_medico(run_medico)
    mensaje(paciente.nombre,paciente.apellido,paciente.email,id,fecha,hora,motivo,medico.nombre)
    cursor.close()
    #database.close()



#busca al paciente por el rut y devuelve una clase paciente con la info
#ejemplo de uso para sacar el nombre:
#paciente=buscar_paciente("rut")
#print(paciente.nombre)
def buscar_paciente(rut):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM paciente WHERE rut = %s",(rut,))
    rows = cursor.fetchall()
    if rows:
        paciente = Paciente(rows[0][0], rows[0][1], rows[0][2], rows[0][3],rows[0][4])
        return paciente  
    else:
        print("Paciente no encontrado.")
        return None
    cursor.close()

def buscar_usuarios(rut):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE rut = %s",(rut,))
    rows = cursor.fetchall()
    if rows:
        usuarios = Usuarios(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5])
        return usuarios  
    else:
        return None
        print("Paciente no encontrado.")
    cursor.close()

def buscar_medico(rut):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM medico WHERE rut = %s",(rut,))
    rows = cursor.fetchall()
    if rows:
        medico = Medico(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5], rows[0][6], rows[0][7], rows[0][8])
        return medico  
    else:
        print("Medico no encontrado.")
    cursor.close()
    #database.close()
def buscar_administrador(rut):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM medico administrador rut = %s",(rut,))
    rows = cursor.fetchall()
    if rows:
        admin = Administrador(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4])
        return admin
    else:
        print("Medico no encontrado.")
    cursor.close()
    #database.close()

def buscar_cita(id):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM citas WHERE id = %s",(id,))
    rows = cursor.fetchall()
    if rows:
        cita = Citas(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4], rows[0][5])
        return cita  
    else:
        print("Cita no encontrado.")
    cursor.close()
    #database.close()
def validar_email(email):
    """
    Valida que el email tenga un formato correcto.
    """
    patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(patron, email) is not None

def mensaje(nombre,apellido, destinatario, cita_id, fecha, hora, motivo, medico):
    remitente = 'correoaaa999@gmail.com'
    password = 'gwjy txfu mozm lnmk'  # Sustituir con una contraseña segura

    # Validar destinatario
    if not validar_email(destinatario):
        raise ValueError(f"Correo electrónico inválido: {destinatario}")

    # Crear asunto y cuerpo del mensaje
    Asunto = 'Confirmación de Reserva'
    body = (
        f"Hola, señor/señora {nombre} {apellido},\n\n"
        f"Este mensaje confirma la cita médica con la ID: {cita_id} con el médico {medico}.\n"
        f"Fecha: {fecha}\n"
        f"Hora: {hora}\n"
        f"Motivo de la visita: {motivo}\n\n"
        f"Saludos cordiales."
    )

    try:
        # Crear el mensaje MIME
        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = Asunto
        mensaje.attach(MIMEText(body, 'plain'))

        # Configurar servidor SMTP
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # Puerto 465 para SSL
        server.login(remitente, password)

        # Enviar el correo
        text = mensaje.as_string()
        server.sendmail(remitente, destinatario, text)
        print("Correo enviado correctamente.")
    except smtplib.SMTPException as e:
        print(f"Error al enviar el correo: {e}")
    finally:
        # Cerrar conexión
        server.quit()



if __name__ == '__main__':

  
    ver_tablas()
    database.close()