// Función para validar contraseña
function validatePassword(password) {
    const errors = [];
    
    // Longitud mínima
    if (password.length < 8) {
        errors.push('Debe tener al menos 8 caracteres');
    }
    
    // Letra minúscula
    if (!/[a-z]/.test(password)) {
        errors.push('Debe contener al menos una letra minúscula');
    }
    
    // Letra mayúscula
    if (!/[A-Z]/.test(password)) {
        errors.push('Debe contener al menos una letra mayúscula');
    }
    
    // Número
    if (!/[0-9]/.test(password)) {
        errors.push('Debe contener al menos un número');
    }
    
    // Carácter especial
    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
        errors.push('Debe contener al menos un carácter especial (!@#$%^&*)');
    }
    
    return errors;
}

// Actualizar indicador de fortaleza de contraseña
function updatePasswordStrength(password) {
    const strengthIndicator = document.getElementById('password-strength');
    const strengthBar = document.getElementById('strength-bar');
    
    if (!password) {
        strengthIndicator.style.display = 'none';
        return;
    }
    
    const errors = validatePassword(password);
    const strength = 5 - errors.length;
    
    strengthIndicator.style.display = 'block';
    
    // Actualizar barra de fortaleza
    const percentage = (strength / 5) * 100;
    strengthBar.style.width = percentage + '%';
    
    // Colores según fortaleza
    if (strength <= 2) {
        strengthBar.className = 'strength-bar weak';
        strengthIndicator.querySelector('.strength-text').textContent = 'Débil';
    } else if (strength <= 3) {
        strengthBar.className = 'strength-bar medium';
        strengthIndicator.querySelector('.strength-text').textContent = 'Media';
    } else if (strength <= 4) {
        strengthBar.className = 'strength-bar good';
        strengthIndicator.querySelector('.strength-text').textContent = 'Buena';
    } else {
        strengthBar.className = 'strength-bar strong';
        strengthIndicator.querySelector('.strength-text').textContent = 'Fuerte';
    }
    
    // Actualizar lista de requisitos
    updateRequirements(password);
}

// Actualizar lista de requisitos visualmente
function updateRequirements(password) {
    const requirements = {
        'req-length': password.length >= 8,
        'req-lowercase': /[a-z]/.test(password),
        'req-uppercase': /[A-Z]/.test(password),
        'req-number': /[0-9]/.test(password),
        'req-special': /[!@#$%^&*(),.?":{}|<>]/.test(password)
    };
    
    Object.keys(requirements).forEach(reqId => {
        const element = document.getElementById(reqId);
        const isValid = requirements[reqId];
        
        element.textContent = (isValid ? '✓' : '✗') + element.textContent.substring(1);
        element.className = isValid ? 'valid' : 'invalid';
    });
}

// Mostrar mensaje de error
function showError(fieldId, message) {
    const field = document.getElementById(fieldId);
    field.classList.add('error');
    
    const errorSpan = document.createElement('span');
    errorSpan.className = 'error-message';
    errorSpan.textContent = message;
    
    field.parentNode.appendChild(errorSpan);
}

// Cuando el documento esté listo
document.addEventListener('DOMContentLoaded', function() {
    // Validación en tiempo real del formulario
    document.getElementById('registerForm').addEventListener('submit', function(e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const email = document.getElementById('email').value;
        
        // Limpiar errores previos
        document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
        document.querySelectorAll('.error-message').forEach(el => el.remove());
        
        let hasErrors = false;
        
        // Validar contraseña
        const passwordErrors = validatePassword(password);
        if (passwordErrors.length > 0) {
            showError('password', 'La contraseña ' + passwordErrors.join(', ').toLowerCase());
            hasErrors = true;
        }
        
        // Validar que las contraseñas coincidan
        if (password !== confirmPassword) {
            showError('confirm_password', 'Las contraseñas no coinciden');
            hasErrors = true;
        }
        
        // Validar formato de email
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            showError('email', 'Por favor ingresa un email válido');
            hasErrors = true;
        }
        
        if (hasErrors) {
            e.preventDefault();
        }
    });
    
    // Validación en tiempo real para confirmar contraseña
    document.getElementById('confirm_password').addEventListener('input', function() {
        const password = document.getElementById('password').value;
        const confirmPassword = this.value;
        
        // Remover mensajes de error previos para este campo
        const errorMsg = this.parentNode.querySelector('.error-message');
        if (errorMsg) errorMsg.remove();
        
        if (confirmPassword && password !== confirmPassword) {
            this.classList.add('error');
            showError('confirm_password', 'Las contraseñas no coinciden');
        } else {
            this.classList.remove('error');
        }
    });
    
    // Validación en tiempo real para email
    document.getElementById('email').addEventListener('blur', function() {
        const email = this.value;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        // Remover mensajes de error previos para este campo
        const errorMsg = this.parentNode.querySelector('.error-message');
        if (errorMsg) errorMsg.remove();
        
        if (email && !emailRegex.test(email)) {
            this.classList.add('error');
            showError('email', 'Por favor ingresa un email válido');
        } else {
            this.classList.remove('error');
        }
    });
    
    // Validación en tiempo real para contraseña con indicador de fortaleza
    document.getElementById('password').addEventListener('input', function() {
        const password = this.value;
        const confirmPassword = document.getElementById('confirm_password').value;
        
        // Remover mensajes de error previos para este campo
        const errorMsg = this.parentNode.querySelector('.error-message');
        if (errorMsg) errorMsg.remove();
        
        // Actualizar indicador de fortaleza
        updatePasswordStrength(password);
        
        // Si hay texto en confirmar contraseña, verificar si coinciden
        if (confirmPassword && password !== confirmPassword) {
            const confirmField = document.getElementById('confirm_password');
            confirmField.classList.add('error');
            showError('confirm_password', 'Las contraseñas no coinciden');
        } else if (confirmPassword) {
            const confirmField = document.getElementById('confirm_password');
            confirmField.classList.remove('error');
            const confirmErrorMsg = confirmField.parentNode.querySelector('.error-message');
            if (confirmErrorMsg) confirmErrorMsg.remove();
        }
    });
});