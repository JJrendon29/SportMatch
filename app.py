from flask import Flask, render_template, request, send_from_directory, jsonify
import os
import mysql.connector
import uuid  

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root15011",
    database="tareas"
)

@app.route('/')
def index():
    try:
        cursor = db.cursor()
        # Consulta SQL modificada para incluir el ID
        consulta = "SELECT id, nombre, edad, deporte, nivel FROM clientes"
        # Ejecutar la consulta
        cursor.execute(consulta)
        # Obtener todos los resultados
        jugadores = cursor.fetchall()
        # Cerrar cursor
        cursor.close()
        # Renderizar la plantilla con los jugadores
        return render_template('index.html', jugadores=jugadores)
    
    except mysql.connector.Error as error:
        # En caso de error, imprime el error y renderiza la plantilla sin jugadores
        print("Error al conectar a MySQL: {}".format(error))
        return render_template('index.html', jugadores=None)

@app.route('/obtener_jugadores')
def obtener_jugadores():
    try:
        cursor = db.cursor()
        # Consulta SQL modificada para incluir el ID
        consulta = "SELECT id, nombre, edad, deporte, nivel FROM clientes"
        # Ejecutar la consulta
        cursor.execute(consulta)
        # Obtener todos los resultados
        jugadores = cursor.fetchall()
        # Cerrar cursor
        cursor.close()
        # Devolver los jugadores en formato JSON
        return jsonify({'jugadores': [list(jugador) for jugador in jugadores]})
    
    except mysql.connector.Error as error:
        # En caso de error, devolver un JSON vacío
        print("Error al conectar a MySQL: {}".format(error))
        return jsonify({'jugadores': []})

@app.route('/images/<filename>')
def serve_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))  # Obtén la ruta del directorio del script actual
    return send_from_directory(os.path.join(root_dir, 'images'), filename)

#buscar por nombre
@app.route('/consultar_nombre', methods=['GET', 'POST'])
def consultar_nombre():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE nombre = %s", (nombre,))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_nombre.html')

#buscar por edad
@app.route('/consultar_edad', methods=['GET', 'POST'])
def consultar_edad():
    if request.method == 'POST':
        edad = request.form['edad']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE edad = %s", (edad,))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_edad.html')

#buscar por deporte
@app.route('/consultar_deporte', methods=['GET', 'POST'])
def consultar_deporte():
    if request.method == 'POST':
        deporte = request.form['deporte']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE deporte = %s", (deporte,))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_deporte.html')

#buscar por nivel
@app.route('/consultar_nivel', methods=['GET', 'POST'])
def consultar_nivel():
    if request.method == 'POST':
        nivel = request.form['nivel']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE nivel = %s", (nivel,))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_nivel.html')

#agregar jugador
@app.route('/agregar_jugador', methods=['GET', 'POST'])
def agregar_jugador():
    # Obtener los últimos 5 jugadores agregados
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes ORDER BY id DESC LIMIT 3")
    jugadores_recientes = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        deporte = request.form['deporte']
        nivel = request.form['nivel']
        
        cursor = db.cursor()
        cursor.execute('INSERT INTO clientes (nombre, edad, deporte, nivel) VALUES (%s, %s, %s, %s)', 
                      (nombre, edad, deporte, nivel))
        db.commit()
        cursor.close()
        
        # Después de agregar, obtenemos la lista actualizada
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes ORDER BY id DESC LIMIT 3")
        jugadores_recientes = cursor.fetchall()
        cursor.close()
        
        return render_template('agregar_jugador.html', jugador_agregado=True, jugadores_recientes=jugadores_recientes)
    
    return render_template('agregar_jugador.html', jugador_agregado=False, jugadores_recientes=jugadores_recientes)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)