# SportMatch

Sistema de gestión de jugadores deportivos con autenticación de usuarios y administración personalizada.

## Características

- **Autenticación segura**: Sistema de login y registro con encriptación de contraseñas
- **Gestión de jugadores**: Agregar, consultar y visualizar jugadores por diferentes criterios
- **Interfaz moderna**: Diseño responsivo con modo claro/oscuro
- **Base de datos**: Almacenamiento seguro en MySQL
- **Seguridad**: Contraseñas hasheadas con bcrypt y validaciones robustas

## Requisitos Previos

- Python 3.7 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd SportMatch
```

### 2. Crear entorno virtual (recomendado)
```bash
python -m venv venv

# En Windows:
venv\Scripts\activate

# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

#### Crear la base de datos en MySQL:
```sql
CREATE DATABASE tareas;
USE tareas;
```

#### Crear tabla de usuarios:
```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Crear tabla de clientes (jugadores):
```sql
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    deporte VARCHAR(50) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    usuario_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);
```

### 5. Configurar credenciales de base de datos

Edita el archivo `app.py` y actualiza las credenciales de conexión:

```python
db = mysql.connector.connect(
    host="localhost",
    user="tu_usuario_mysql",      # Cambia por tu usuario
    password="tu_password_mysql", # Cambia por tu contraseña
    database="tareas"
)
```

### 6. Ejecutar la aplicación
```bash
python app.py
```

La aplicación estará disponible en: `http://localhost:5001`

## Dependencias

```
flask
mysql-connector-python
pytest
flask-login
werkzeug
```

## Estructura del Proyecto

```
SportMatch/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Documentación
├── static/               # Archivos estáticos (CSS, JS, imágenes)
│   ├── styles.css        # Estilos globales
│   ├── theme-switch.css  # Estilos del interruptor de tema
│   ├── theme-switch.js   # JavaScript del interruptor de tema
│   ├── login-styles.css  # Estilos específicos del login
│   ├── register-styles.css # Estilos específicos del registro
│   ├── cliente.css       # Estilos para páginas de clientes
│   ├── jugadores-table.css # Estilos para tablas de jugadores
│   └── list.css          # Estilos para páginas de consulta
├── templates/            # Plantillas HTML
│   ├── index.html        # Página principal
│   ├── login.html        # Página de inicio de sesión
│   ├── register.html     # Página de registro
│   ├── agregar_jugador.html # Formulario agregar jugador
│   ├── cliente.html      # Resultados de consultas
│   └── consultar_*.html  # Formularios de consulta
├── images/               # Imágenes del proyecto
│   ├── logo.png          # Logo de SportMatch
│   └── home.png          # Icono de inicio
└── tests/                # Pruebas unitarias
    └── test_app.py       # Tests de la aplicación
```

## Uso de la Aplicación

### Registro de Usuario
1. Accede a `/register`
2. Completa el formulario con:
   - Nombre de usuario (único)
   - Email (único)
   - Contraseña (mínimo 8 caracteres, mayúscula, minúscula, número y carácter especial)
3. Confirma tu contraseña

### Inicio de Sesión
1. Accede a `/login`
2. Ingresa tu usuario y contraseña
3. Serás redirigido al dashboard principal

### Gestión de Jugadores
- **Agregar**: Completa el formulario con nombre, edad, deporte y nivel
- **Consultar**: Busca por nombre, edad, deporte o nivel
- **Visualizar**: Ve todos tus jugadores en la página principal

## Seguridad

- Las contraseñas se hashean usando bcrypt
- Sesiones seguras con Flask-Login
- Validaciones tanto en frontend como backend
- Cada usuario solo puede ver sus propios jugadores

## Características Especiales

- **Modo Oscuro**: Interruptor en la esquina superior derecha
- **Diseño Responsivo**: Optimizada para móviles y escritorio
- **Validación en Tiempo Real**: Feedback inmediato en formularios
- **Indicador de Fortaleza**: Muestra la seguridad de tu contraseña

## Base de Datos

La aplicación usa MySQL con las siguientes tablas:

- **usuarios**: Almacena información de autenticación
- **clientes**: Almacena información de los jugadores

## 🔧 Desarrollo

### Ejecutar pruebas
```bash
pytest
```

### Configuración de desarrollo
```python
# En app.py, para debugging:
app.run(debug=True, host='0.0.0.0', port=5001)
```

## Notas Importantes

1. **Cambia la clave secreta** en `app.py`:
   ```python
   app.secret_key = 'tu_clave_secreta_aqui_cambiala'
   ```

2. **Actualiza las credenciales de MySQL** según tu configuración local

3. **Asegúrate** de que MySQL esté ejecutándose antes de iniciar la aplicación
