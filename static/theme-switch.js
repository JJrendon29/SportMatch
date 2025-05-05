// Manejar el cambio de tema
document.addEventListener('DOMContentLoaded', function() {
    // Buscar el elemento del interruptor de tema
    const themeSwitch = document.getElementById('theme-switch');
    
    // Verificar si hay una preferencia guardada en localStorage
    const currentTheme = localStorage.getItem('theme');
    
    // Si hay una preferencia guardada, aplicarla
    if (currentTheme) {
        document.body.classList.add(currentTheme);
        
        // Actualizar la posición del interruptor si el tema es oscuro
        if (currentTheme === 'dark-theme') {
            themeSwitch.checked = true;
            document.getElementById('theme-icon').className = 'fas fa-moon slider-icon';
        }
    }
    
    // Escuchar eventos de cambio en el interruptor
    themeSwitch.addEventListener('change', function(e) {
        if (e.target.checked) {
            // Cambiar a tema oscuro
            document.body.classList.remove('light-theme');
            document.body.classList.add('dark-theme');
            localStorage.setItem('theme', 'dark-theme');
            document.getElementById('theme-icon').className = 'fas fa-moon slider-icon';
        } else {
            // Cambiar a tema claro
            document.body.classList.remove('dark-theme');
            document.body.classList.add('light-theme');
            localStorage.setItem('theme', 'light-theme');
            document.getElementById('theme-icon').className = 'fas fa-sun slider-icon';
        }
    });
});

// Agregar esto a tu archivo theme-switch.js

document.addEventListener('DOMContentLoaded', function() {
    const themeSwitch = document.getElementById('theme-switch');
    const logo = document.querySelector('.custom-logo');
    
    // Aplicar efectos al logo basado en el tema actual
    function updateLogoStyles(isDarkTheme) {
        if (isDarkTheme) {
            // Logo en modo oscuro
            if (logo) {
                // Opción 1: Aplicar un fondo ligero detrás del logo
                logo.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
                logo.style.padding = '5px';
                logo.style.border = '1px solid rgba(255, 255, 255, 0.2)';
                
                // Opción 2: Aplicar un filtro para mejorar visibilidad
                logo.style.filter = 'brightness(1.1) drop-shadow(0 0 3px rgba(255, 255, 255, 0.7))';
            }
        } else {
            // Logo en modo claro (restaurar valores predeterminados)
            if (logo) {
                logo.style.backgroundColor = '';
                logo.style.padding = '';
                logo.style.border = '';
                logo.style.filter = '';
            }
        }
    }
    
    // Verificar el tema actual almacenado
    const currentTheme = localStorage.getItem('theme');
    if (currentTheme === 'dark-theme') {
        updateLogoStyles(true);
    }
    
    // Escuchar cambios en el interruptor de tema
    themeSwitch.addEventListener('change', function(e) {
        updateLogoStyles(e.target.checked);
    });
});