// ============================================
// CHATBOT ACADÉMICO UNAL - JAVASCRIPT
// ============================================

const API_URL = 'http://localhost:8000';

// ============ INICIALIZACIÓN ============
document.addEventListener('DOMContentLoaded', () => {
    verificarEstado();
});

// ============ VERIFICAR ESTADO DEL SERVIDOR ============
async function verificarEstado() {
    const badge = document.getElementById('estadoBadge');
    const texto = document.getElementById('estadoTexto');

    try {
        const respuesta = await fetch(`${API_URL}/api/estado`);
        const datos = await respuesta.json();

        if (respuesta.ok) {
            badge.classList.add('activo');
            texto.textContent = `Sistema activo · ${datos.documentos_cargados} docs`;
        }
    } catch (error) {
        badge.classList.add('error');
        texto.textContent = 'Sin conexión';
    }
}

// ============ ENVIAR PREGUNTA ============
async function enviarPregunta() {
    const input = document.getElementById('inputPregunta');
    const pregunta = input.value.trim();

    if (!pregunta) return;

    // Ocultar bienvenida si existe
    const bienvenida = document.querySelector('.mensaje-bienvenida');
    if (bienvenida) bienvenida.remove();

    // Mostrar mensaje del usuario
    agregarMensaje(pregunta, 'usuario');
    input.value = '';
    ajustarAltura(input);

    // Deshabilitar botón
    const btn = document.getElementById('btnEnviar');
    btn.disabled = true;

    // Mostrar indicador de carga
    const idCarga = mostrarCargando();

    try {
        const respuesta = await fetch(`${API_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pregunta })
        });

        const datos = await respuesta.json();

        // Quitar indicador de carga
        quitarCargando(idCarga);

        if (respuesta.ok) {
            agregarMensaje(datos.respuesta, 'bot');
        } else {
            agregarMensaje('Ocurrió un error al procesar tu pregunta. Intenta de nuevo.', 'bot');
        }

    } catch (error) {
        quitarCargando(idCarga);
        agregarMensaje('No se pudo conectar con el servidor. Verifica que el backend esté activo.', 'bot');
    }

    btn.disabled = false;
    input.focus();
}

// ============ AGREGAR MENSAJE AL CHAT ============
function agregarMensaje(texto, tipo) {
    const area = document.getElementById('mensajesArea');

    const mensaje = document.createElement('div');
    mensaje.classList.add('mensaje', tipo);

    const avatar = document.createElement('div');
    avatar.classList.add('mensaje-avatar');
    avatar.textContent = tipo === 'usuario' ? '👤' : '🤖';

    const burbuja = document.createElement('div');
    burbuja.classList.add('mensaje-burbuja');
    burbuja.innerHTML = formatearTexto(texto);

    mensaje.appendChild(avatar);
    mensaje.appendChild(burbuja);
    area.appendChild(mensaje);

    // Scroll al final
    area.scrollTop = area.scrollHeight;
}

// ============ FORMATEAR TEXTO ============
function formatearTexto(texto) {
    return texto
        .replace(/\n\n/g, '</p><p>')
        .replace(/\n/g, '<br>')
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\*(.*?)\*/g, '<em>$1</em>')
        .replace(/^(.+)$/, '<p>$1</p>');
}

// ============ INDICADOR DE CARGA ============
function mostrarCargando() {
    const area = document.getElementById('mensajesArea');
    const id = 'carga_' + Date.now();

    const mensaje = document.createElement('div');
    mensaje.classList.add('mensaje', 'bot');
    mensaje.id = id;

    const avatar = document.createElement('div');
    avatar.classList.add('mensaje-avatar');
    avatar.textContent = '🤖';

    const burbuja = document.createElement('div');
    burbuja.classList.add('mensaje-burbuja');
    burbuja.innerHTML = `
        <div class="cargando-indicador">
            <span></span>
            <span></span>
            <span></span>
        </div>
    `;

    mensaje.appendChild(avatar);
    mensaje.appendChild(burbuja);
    area.appendChild(mensaje);
    area.scrollTop = area.scrollHeight;

    return id;
}

function quitarCargando(id) {
    const elemento = document.getElementById(id);
    if (elemento) elemento.remove();
}

// ============ ENVIAR SUGERENCIA ============
function enviarSugerencia(btn) {
    const texto = btn.textContent.trim().replace(/^[^\s]+\s/, '');
    const input = document.getElementById('inputPregunta');
    input.value = texto;
    enviarPregunta();
}

// ============ MANEJO DE TECLADO ============
function manejarTecla(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        enviarPregunta();
    }
}

// ============ AJUSTAR ALTURA TEXTAREA ============
function ajustarAltura(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
}