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

def ejemplo():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM paciente")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()


def atributos():
    cursor = database.cursor()
    cursor.execute("DESCRIBE paciente")
    rows = cursor.fetchall()
    print("Atributos de la tabla paciente:")
    for row in rows: 
        print(row)

    cursor.close()


def insertar_paciente(rut,nombre,email, telefono):
    cursor = database.cursor()
    valores = (rut,nombre,email, telefono)
    cursor.execute("INSERT INTO paciente (run, nombre, correo, telefono) VALUES (%s, %s, %s, %s)",valores)
    print("Paciente "+ nombre+ " insertado")
    database.commit()
    cursor.close()


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
        print("Paciente no encontrado.")
    cursor.close()

if __name__ == '__main__':
    ejemplo()
    pa=buscar_paciente("222222222")
    print(pa.nombre)
    database.close
    
