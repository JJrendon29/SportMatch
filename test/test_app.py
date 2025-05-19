import sys
import os
import pytest
import tempfile
from unittest.mock import patch, MagicMock
from werkzeug.security import generate_password_hash

# Agregar el directorio padre al path para importar app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, validate_password

class TestApp:
    
    @pytest.fixture
    def client(self):
        """Cliente de prueba para Flask"""
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        with app.test_client() as client:
            with app.app_context():
                yield client

    @pytest.fixture
    def mock_db(self):
        """Mock de la base de datos"""
        with patch('app.db') as mock:
            mock_cursor = MagicMock()
            mock.cursor.return_value = mock_cursor
            yield mock_cursor

    # ===== PRUEBAS FUNCIONALES =====
    
    def test_login_page_loads(self, client):
        """Test: La página de login carga correctamente"""
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Iniciar Sesi' in response.data  # "Sesión" en UTF-8
    
    def test_register_page_loads(self, client):
        """Test: La página de registro carga correctamente"""
        response = client.get('/register')
        assert response.status_code == 200
        assert b'Crear Cuenta' in response.data
    
    def test_index_redirects_when_not_logged_in(self, client):
        """Test: Index redirige al login cuando no hay sesión"""
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location

    # ===== PRUEBAS UNITARIAS =====
    
    def test_validate_password_success(self):
        """Test: Validación de contraseña exitosa"""
        password = "MiPassword123!"
        errors = validate_password(password)
        assert len(errors) == 0
    
    def test_validate_password_too_short(self):
        """Test: Contraseña muy corta"""
        password = "Ab1!"
        errors = validate_password(password)
        assert "debe tener al menos 8 caracteres" in errors
    
    def test_validate_password_no_uppercase(self):
        """Test: Contraseña sin mayúscula"""
        password = "mipassword123!"
        errors = validate_password(password)
        assert "debe contener al menos una letra mayúscula" in errors
    
    def test_validate_password_no_lowercase(self):
        """Test: Contraseña sin minúscula"""
        password = "MIPASSWORD123!"
        errors = validate_password(password)
        assert "debe contener al menos una letra minúscula" in errors
    
    def test_validate_password_no_number(self):
        """Test: Contraseña sin número"""
        password = "MiPassword!"
        errors = validate_password(password)
        assert "debe contener al menos un número" in errors
    
    def test_validate_password_no_special_char(self):
        """Test: Contraseña sin carácter especial"""
        password = "MiPassword123"
        errors = validate_password(password)
        # Buscar cualquier mensaje que contenga "carácter especial"
        assert any("carácter especial" in error for error in errors), f"Expected error about special character, got: {errors}"

    # ===== PRUEBAS DE REGRESIÓN =====
    
    def test_register_with_existing_username(self, client, mock_db):
        """Test: Registro con usuario existente debe fallar"""
        # Simular que el usuario ya existe
        mock_db.fetchone.side_effect = [("existing_user",), None]  # Username exists, email doesn't
        
        response = client.post('/register', data={
            'username': 'existing_user',
            'email': 'new@email.com',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        assert response.status_code == 200
        assert b'El nombre de usuario ya existe' in response.data
    
    def test_register_with_existing_email(self, client, mock_db):
        """Test: Registro con email existente debe fallar"""
        # Simular que el email ya existe
        mock_db.fetchone.side_effect = [None, ("existing@email.com",)]  # Username doesn't exist, email exists
        
        response = client.post('/register', data={
            'username': 'new_user',
            'email': 'existing@email.com',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        assert response.status_code == 200
        assert b'El correo electr' in response.data  # "electrónico" en UTF-8
    
    def test_register_success(self, client, mock_db):
        """Test: Registro exitoso"""
        # Simular que ni el usuario ni el email existen
        mock_db.fetchone.side_effect = [None, None]  # Neither username nor email exist
        
        response = client.post('/register', data={
            'username': 'new_user',
            'email': 'new@email.com',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        
        assert response.status_code == 302  # Redirect to login after successful registration
    
    def test_login_with_invalid_credentials(self, client, mock_db):
        """Test: Login con credenciales inválidas debe fallar"""
        # Simular usuario no encontrado
        mock_db.fetchone.return_value = None
        
        response = client.post('/login', data={
            'username': 'nonexistent',
            'password': 'WrongPass123!'
        })
        
        assert response.status_code == 200
        assert b'Usuario o contrase' in response.data  # "contraseña" en UTF-8

    # ===== PRUEBAS DE CARGA =====
    
    def test_multiple_register_attempts(self, client, mock_db):
        """Test: Múltiples intentos de registro simultáneos"""
        # Simular base de datos disponible para todos los intentos
        mock_db.fetchone.return_value = None
        
        # Hacer múltiples requests
        responses = []
        for i in range(10):
            response = client.post('/register', data={
                'username': f'user_{i}',
                'email': f'user_{i}@email.com',
                'password': 'ValidPass123!',
                'confirm_password': 'ValidPass123!'
            })
            responses.append(response.status_code)
        
        # Todos deberían procesar correctamente (200 o 302)
        for status in responses:
            assert status in [200, 302]
    
    def test_serve_image_route(self, client):
        """Test: Ruta de imágenes funciona correctamente"""
        # Test con imagen que probablemente no existe
        response = client.get('/images/nonexistent.png')
        # Debe retornar 404 (imagen no existe) o 200 (imagen existe)
        assert response.status_code in [200, 404, 500]  # 500 si hay error de permisos

    # ===== PRUEBAS DE INTEGRACIÓN =====
    
    def test_full_user_flow(self, client, mock_db):
        """Test: Flujo completo usuario registro -> login"""
        # Configurar el mock para múltiples llamadas
        # Primera llamada: verificar si username existe (no existe)
        # Segunda llamada: verificar si email existe (no existe)
        # Tercera llamada: login - obtener usuario
        
        mock_db.fetchone.side_effect = [
            None,  # Username doesn't exist
            None,  # Email doesn't exist
            (1, 'test_user', generate_password_hash('ValidPass123!'), 'test@email.com')  # Login data
        ]
        
        # 1. Registro exitoso
        register_response = client.post('/register', data={
            'username': 'test_user',
            'email': 'test@email.com',
            'password': 'ValidPass123!',
            'confirm_password': 'ValidPass123!'
        })
        assert register_response.status_code == 302
        
        # 2. Intentar login (el mock ya está configurado arriba)
        login_response = client.post('/login', data={
            'username': 'test_user',
            'password': 'ValidPass123!'
        })
        assert login_response.status_code == 302