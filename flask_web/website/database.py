import mysql.connector


database = mysql.connector.connect(
    host='sql10.freemysqlhosting.net',
    user='sql10744621',
    password='3V8KsTBuW1',
    database='sql10744621'
)
class Paciente:
    def __init__(self, rut, nombre, email, telefono):
        self.rut = rut
        self.nombre = nombre
        self.email = email
        self.telefono = telefono

class Medico:
    def __init__(self, rut, nombre, correo, contraseña, especialidad):
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña
        self.especialidad = especialidad

class Administrador:
    def __init__(self, rut, nombre, correo, contraseña):
        self.rut = rut
        self.nombre = nombre
        self.correo = correo
        self.contraseña = contraseña

class Citas:
    def __init__(self, id, medico, paciente, hora, fecha, motivo):
        self.id = id
        self.medico = medico
        self.paciente = paciente
        self.hora = hora
        self.fecha = fecha
        self.motivo = motivo

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


def atributos():
    cursor = database.cursor()
    cursor.execute("DESCRIBE administrador")
    rows = cursor.fetchall()
    print("Atributos de la tabla citas:")
    for row in rows: 
        print(row)

    cursor.close()
    #database.close()


def insertar_paciente(rut,nombre,apellido,email, telefono):
    cursor = database.cursor()
    cursor.execute("INSERT INTO paciente (run, nombre, apellido, correo, telefono) VALUES (%s, %s, %s, %s, %s)",(rut,nombre,apellido,email, telefono))
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

def insertar_medico(rut, nombre, correo, contraseña, especialidad):
    cursor = database.cursor()
    cursor.execute("INSERT INTO medico (rut, nombre, correo, contraseña, especialidad) VALUES (%s, %s, %s, %s, %s)",(rut, nombre, correo, contraseña, especialidad))
    print("Medico "+ nombre+ " insertado")
    database.commit()
    cursor.close()
    #database.close()

def insertar_cita(id, run_medico, run_paciente, hora, fecha, motivo):
    cursor = database.cursor()
    cursor.execute("INSERT INTO citas (id, medico, paciente_rut, hora, fecha, motivo) VALUES (%s, %s, %s, %s, %s, %s)", (id, run_medico, run_paciente, hora, fecha, motivo))
    database.commit()
    #print("Cita "+ id + " insertada")
    database.commit()
    cursor.close()
    #database.close()


#busca al paciente por el rut y debuelbe una clase paciente con la info
#ejeplo de uso para sacar el nombre:
#paciente=buscar_paciente("rut")
#print(paciente.nombre)
def buscar_paciente(rut):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM paciente WHERE run = %s",(rut,))
    rows = cursor.fetchall()
    if rows:
        paciente = Paciente(rows[0][0], rows[0][1], rows[0][2], rows[0][3])
        return paciente  
    else:
        return None
        print("Paciente no encontrado.")
    cursor.close()

def buscar_medico(rut):
    cursor = database.cursor()
    cursor.execute("SELECT * FROM medico WHERE rut = %s",(rut,))
    rows = cursor.fetchall()
    if rows:
        medico = Medico(rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4])
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

if __name__ == '__main__':
    ver_tablas()
    
    
    
