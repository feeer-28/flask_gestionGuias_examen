let guias = [];
let instructores = [];
let mensaje = null;

listarInstructores();
listarGuias();

function validarGuia() {
    if (document.getElementById("txtCodigo").value == "") {
        mensaje = "Debe ingresar código de la Guía";
        return false;
    } else if (document.getElementById("txtTitulo").value == "") {
        mensaje = "Debe ingresar Título de la Guía";
        return false;
    } else if (document.getElementById("txtContenido").value == "") {
        mensaje = "Debe ingresar el Contenido de la Guía";
        return false;
    } else {
        return true;
    }
}

function validarInstructor() {
    if (document.getElementById("txtNombre").value == "") {
        mensaje = "Debe ingresar el nombre del Instructor";
        return false;
    } else if (document.getElementById("txtCorreo").value == "") {
        mensaje = "Debe ingresar el correo del Instructor";
        return false;
    } else {
        return true;
    }
}

function listarGuias() {
    const url = "/guia/";
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((respuesta) => respuesta.json())
        .then((resultado) => {
            guias = resultado.guias;
            console.log(guias);
            mostrarGuiasTabla();
        })
        .catch((error) => {
            console.error(error);
        });
}

function listarInstructores() {
    const url = "/instructor/";
    fetch(url, {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
        },
    })
        .then((respuesta) => respuesta.json())
        .then((resultado) => {
            instructores = resultado.instructores;
            console.log(instructores);
        })
        .catch((error) => {
            console.error(error);
        });
}

function mostrarGuiasTabla() {
    let datos = "";

    guias.forEach((guia) => {
        datos += "<tr>";
        datos += "<td>" + guia.codigo + "</td>";
        datos += "<td>" + guia.titulo + "</td>";
        datos += "<td>" + guia.contenido + "</td>";
        datos += "</tr>";
    });
    document.getElementById("datosGuias").innerHTML = datos;
}

/**
 * Función que se encarga de hacer
 * una petición al backend para
 * agregar una guía.
 */
function agregarGuia() {
    if (validarGuia()) {
        const url = "/guia/";
        const guia = {
            codigo: document.getElementById("txtCodigo").value,
            titulo: document.getElementById("txtTitulo").value,
            contenido: document.getElementById("txtContenido").value,
        };
        fetch(url, {
            method: "POST",
            body: JSON.stringify(guia),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((respuesta) => respuesta.json())
            .then((resultado) => {
                if (resultado.estado) {
                    location.href = "/guias/";
                } else {
                    swal.fire("Add Guía", resultado.mensaje, "warning");
                }
            })
            .catch((error) => {
                console.error(error);
            });
    } else {
        swal.fire("Add Guía", mensaje, "warning");
    }
}

/**
 * Función que se encarga de hacer
 * una petición al backend para
 * agregar un instructor.
 */
function agregarInstructor() {
    if (validarInstructor()) {
        const instructor = {
            nombre: document.getElementById("txtNombre").value,
            correo: document.getElementById("txtCorreo").value,
        };
        const url = "/instructor/";
        fetch(url, {
            method: "POST",
            body: JSON.stringify(instructor),
            headers: {
                "Content-Type": "application/json",
            },
        })
            .then((respuesta) => respuesta.json())
            .then((resultado) => {
                if (resultado.estado) {
                    location.href = "/instructores/";
                } else {
                    swal.fire("Add Instructor", resultado.mensaje, "warning");
                }
            })
            .catch((error) => {
                console.error(error);
            });
    } else {
        swal.fire("Add Instructor", mensaje, "warning");
    }
}