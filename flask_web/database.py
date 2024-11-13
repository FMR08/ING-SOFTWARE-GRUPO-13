import mysql.connector

database = mysql.connector.connect(

    host='sql10.freemysqlhosting.net',
    user='sql10744621',
    password='3V8KsTBuW1',
    database='sql10744621'
)
def ejemplo():
    cursor = database.cursor()
    cursor.execute("SELECT * FROM paciente")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.close()
    database.close()
if __name__ == '__main__':
    ejemplo()
