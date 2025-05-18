from flask import Flask, render_template, request, send_from_directory, jsonify, redirect, url_for, flash, session
import os
import mysql.connector
import uuid  
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'Pruebas15011'

# Configurar Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root15011",
    database="tareas"
)

# Clase User para Flask-Login
class User(UserMixin):
    def __init__(self, id, username, email):
        self.id = id
        self.username = username
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor = db.cursor()
    cursor.execute("SELECT id, username, email FROM usuarios WHERE id = %s", (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    
    if user_data:
        return User(user_data[0], user_data[1], user_data[2])
    return None

# Rutas de autenticación
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor()
        cursor.execute("SELECT id, username, password, email FROM usuarios WHERE username = %s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        
        if user_data and check_password_hash(user_data[2], password):
            user = User(user_data[0], user_data[1], user_data[3])
            login_user(user)
            flash('¡Bienvenido {}!'.format(user.username), 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = db.cursor()
        
        # Verificar si el usuario ya existe
        cursor.execute("SELECT username FROM usuarios WHERE username = %s", (username,))
        existing_user = cursor.fetchone()
        
        # Verificar si el email ya existe
        cursor.execute("SELECT email FROM usuarios WHERE email = %s", (email,))
        existing_email = cursor.fetchone()
        
        if existing_user:
            flash('El nombre de usuario ya existe', 'error')
        elif existing_email:
            flash('El correo electrónico ya está registrado', 'error')
        else:
            # Crear nuevo usuario
            try:
                hashed_password = generate_password_hash(password)
                cursor.execute("INSERT INTO usuarios (username, password, email) VALUES (%s, %s, %s)", 
                             (username, hashed_password, email))
                db.commit()
                flash('Usuario registrado exitosamente. ¡Ahora puedes iniciar sesión!', 'success')
                cursor.close()
                return redirect(url_for('login'))
            except mysql.connector.IntegrityError as e:
                if 'Duplicate entry' in str(e) and 'username' in str(e):
                    flash('El nombre de usuario ya existe', 'error')
                elif 'Duplicate entry' in str(e) and 'email' in str(e):
                    flash('El correo electrónico ya está registrado', 'error')
                else:
                    flash('Error al registrar usuario. Intenta nuevamente.', 'error')
        
        cursor.close()
    
    return render_template('register.html')

# Rutas principales (protegidas)
@app.route('/')
@login_required
def index():
    try:
        cursor = db.cursor()
        # Obtener solo los jugadores del usuario actual
        consulta = "SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE usuario_id = %s OR usuario_id IS NULL"
        cursor.execute(consulta, (current_user.id,))
        jugadores = cursor.fetchall()
        cursor.close()
        return render_template('index.html', jugadores=jugadores)
    
    except mysql.connector.Error as error:
        print("Error al conectar a MySQL: {}".format(error))
        return render_template('index.html', jugadores=None)

@app.route('/obtener_jugadores')
@login_required
def obtener_jugadores():
    try:
        cursor = db.cursor()
        consulta = "SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE usuario_id = %s OR usuario_id IS NULL"
        cursor.execute(consulta, (current_user.id,))
        jugadores = cursor.fetchall()
        cursor.close()
        return jsonify({'jugadores': [list(jugador) for jugador in jugadores]})
    
    except mysql.connector.Error as error:
        print("Error al conectar a MySQL: {}".format(error))
        return jsonify({'jugadores': []})

@app.route('/images/<filename>')
def serve_image(filename):
    root_dir = os.path.dirname(os.path.abspath(__file__))
    return send_from_directory(os.path.join(root_dir, 'images'), filename)

# Buscar por nombre
@app.route('/consultar_nombre', methods=['GET', 'POST'])
@login_required
def consultar_nombre():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE nombre = %s AND (usuario_id = %s OR usuario_id IS NULL)", 
                      (nombre, current_user.id))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_nombre.html')

# Buscar por edad
@app.route('/consultar_edad', methods=['GET', 'POST'])
@login_required
def consultar_edad():
    if request.method == 'POST':
        edad = request.form['edad']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE edad = %s AND (usuario_id = %s OR usuario_id IS NULL)", 
                      (edad, current_user.id))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_edad.html')

# Buscar por deporte
@app.route('/consultar_deporte', methods=['GET', 'POST'])
@login_required
def consultar_deporte():
    if request.method == 'POST':
        deporte = request.form['deporte']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE deporte = %s AND (usuario_id = %s OR usuario_id IS NULL)", 
                      (deporte, current_user.id))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_deporte.html')

# Buscar por nivel
@app.route('/consultar_nivel', methods=['GET', 'POST'])
@login_required
def consultar_nivel():
    if request.method == 'POST':
        nivel = request.form['nivel']
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE nivel = %s AND (usuario_id = %s OR usuario_id IS NULL)", 
                      (nivel, current_user.id))
        clientes = cursor.fetchall()
        cursor.close()
        return render_template('cliente.html', clientes=clientes)
    return render_template('consultar_nivel.html')

# Agregar jugador
@app.route('/agregar_jugador', methods=['GET', 'POST'])
@login_required
def agregar_jugador():
    # Obtener los últimos 3 jugadores agregados por este usuario
    cursor = db.cursor()
    cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE usuario_id = %s ORDER BY id DESC LIMIT 3", 
                  (current_user.id,))
    jugadores_recientes = cursor.fetchall()
    cursor.close()
    
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        deporte = request.form['deporte']
        nivel = request.form['nivel']
        
        cursor = db.cursor()
        cursor.execute('INSERT INTO clientes (nombre, edad, deporte, nivel, usuario_id) VALUES (%s, %s, %s, %s, %s)', 
                      (nombre, edad, deporte, nivel, current_user.id))
        db.commit()
        cursor.close()
        
        # Después de agregar, obtenemos la lista actualizada
        cursor = db.cursor()
        cursor.execute("SELECT id, nombre, edad, deporte, nivel FROM clientes WHERE usuario_id = %s ORDER BY id DESC LIMIT 3", 
                      (current_user.id,))
        jugadores_recientes = cursor.fetchall()
        cursor.close()
        
        flash('Jugador agregado exitosamente', 'success')
        return render_template('agregar_jugador.html', jugador_agregado=True, jugadores_recientes=jugadores_recientes)
    
    return render_template('agregar_jugador.html', jugador_agregado=False, jugadores_recientes=jugadores_recientes)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)