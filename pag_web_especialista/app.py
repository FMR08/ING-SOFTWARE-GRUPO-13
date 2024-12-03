from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

# Conexión a la base de datos
db_config = {
    "host": "sql10.freemysqlhosting.net",
    "user": "sql10744621",
    "password": "3V8KsTBuW1",
    "database": "sql10744621"
}

@app.route("/api/horarios", methods=["GET"])
def obtener_horarios():
    conexion = mysql.connector.connect(**db_config)
    cursor = conexion.cursor(dictionary=True)

    # Consulta los horarios desde la base de datos
    cursor.execute("""
        SELECT hora, paciente, contacto, nota 
        FROM horarios
        WHERE hora BETWEEN '08:00:00' AND '22:00:00'
    """)
    horarios = cursor.fetchall()

    # Consulta para obtener los horarios agrupados por día
    cursor.execute("""
           SELECT DATE(hora) AS dia, TIME(hora) AS hora, paciente
           FROM horarios
           WHERE hora BETWEEN '2023-01-01' AND '2030-12-31'
           ORDER BY dia, hora
       """)
    horarios = cursor.fetchall()

    cursor.close()
    conexion.close()

    # Organizar los datos por día
    horarios_por_dia = {}
    for horario in horarios:
        dia = horario["dia"].strftime("%Y-%m-%d")
        if dia not in horarios_por_dia:
            horarios_por_dia[dia] = []
        horarios_por_dia[dia].append({
            "hora": horario["hora"].strftime("%H:%M"),
            "paciente": horario["paciente"]
        })
    return jsonify(horarios, horarios_por_dia)


if __name__ == "__main__":
    app.run(debug=True)

