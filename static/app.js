let guias = [];
let mensaje = null;

// Inicialización al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    listarGuias();
});

// Validación de formulario
function validarGuia() {
    const formulario = document.forms['formGuia'];
    if (!formulario) return false;

    if (formulario.nombre.value.trim() === "") {
        mensaje = "Debe ingresar el nombre de la guía";
        return false;
    }
    if (formulario.descripcion.value.trim() === "") {
        mensaje = "Debe ingresar la descripción";
        return false;
    }
    if (formulario.programa.value === "") {
        mensaje = "Debe seleccionar un programa";
        return false;
    }
    if (!formulario.archivo.files[0]) {
        mensaje = "Debe seleccionar un archivo PDF";
        return false;
    }
    return true;
}

// Listar guías desde la API
async function listarGuias() {
    try {
        const response = await fetch('/api/guias/');
        const data = await response.json();
        
        if (data.estado) {
            guias = data.guias;
            mostrarGuiasTabla();
        } else {
            mostrarError(data.mensaje);
        }
    } catch (error) {
        mostrarError(`Error al cargar guías: ${error.message}`);
    }
}

// Mostrar guías en la tabla
function mostrarGuiasTabla() {
    const tbody = document.getElementById('guias-body');
    if (!tbody) return;

    let contenido = '';
    
    guias.forEach(guia => {
        contenido += `
        <tr>
            <td>${guia.nombre}</td>
            <td>${guia.descripcion}</td>
            <td>${guia.programa}</td>
            <td>${guia.instructor?.nombres || 'Sin instructor'}</td>
            <td>${guia.instructor?.regional?.nombre || 'Sin regional'}</td>
            <td>${new Date(guia.fecha).toLocaleDateString('es-CO', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            })}</td>
            <td class="text-center">
                <a href="/static/uploads/${guia.archivo}" 
                   target="_blank" 
                   class="btn btn-link">
                    <i class="fas fa-file-pdf fa-2x text-danger"></i>
                </a>
            </td>
        </tr>`;
    });

    tbody.innerHTML = contenido || `
        <tr>
            <td colspan="7" class="text-center">No hay guías registradas</td>
        </tr>`;
}

// Manejar envío de formulario
async function agregarGuia(event) {
    event.preventDefault();

    if (!validarGuia()) {
        mostrarError(mensaje);
        return;
    }

    const formulario = document.forms['formGuia'];
    const formData = new FormData(formulario);

    try {
        const response = await fetch('/api/guias/', {
            method: 'POST',
            body: formData
        });

        const resultado = await response.json();
        console.log("Respuesta del servidor:", resultado);

        if (resultado.estado) {
            mostrarExito(resultado.mensaje);
            formulario.reset();
            await listarGuias();
        } else {
            mostrarError(resultado.mensaje);
        }
    } catch (error) {
        console.error("Error al subir la guía:", error);
        mostrarError(`Error de conexión: ${error.message}`);
    }
}
