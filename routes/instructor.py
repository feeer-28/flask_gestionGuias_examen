from app import app
from flask import render_template, request, session, redirect
from models.instructor import Instructor
from dotenv import load_dotenv
from models.regional import Regional

load_dotenv()

@app.route("/")
def inicio():
    return render_template("frmIniciarSesion.html")


@app.route("/iniciarSesion/", methods=['POST'])
def iniciarSesion():
    try:
        mensaje = None
        datos = request.form

        # Validar que los datos requeridos estén presentes
        if 'txtUser' not in datos or 'txtPassword' not in datos:
            mensaje = "Debe ingresar usuario y contraseña"
            return render_template("frmIniciarSesion.html", mensaje=mensaje)

        # Buscar al instructor por el campo 'usuario'
        instructor = Instructor.objects(usuario=datos['txtUser']).first()
        if instructor is None:
            mensaje = "El usuario no existe"
        else:
            # Verificar si la contraseña es correcta
            if instructor.password == datos['txtPassword']:
                session["user"] = instructor.usuario  # Guardar el usuario en la sesión
                mensaje = "Bienvenido al sistema"
                return redirect("/home/")  # Redirigir al home si el inicio de sesión es exitoso
            else:
                mensaje = "Contraseña incorrecta"
    except Exception as error:
        mensaje = f"Error inesperado: {error}"

    # Renderizar el formulario con el mensaje de error
    return render_template("frmIniciarSesion.html", mensaje=mensaje)



@app.route("/instructor/", methods=['POST'])
def addInstructor():
    try:
        mensaje=None
        estado=False
        datos= request.get_json(force=True)
        instructor = instructor(**datos)
        instructor.save()
        estado=True
        mensaje="instructor agregado correctamente"       
        
    except Exception as error:
        mensaje=str(error) 
        
    return {"estado":estado, "mensaje":mensaje}


@app.route("/home/")
def home():
    if("user" in session):
        return render_template("frmContenido.html")
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/salir/")
def exit():
    session.clear()
    mensaje="Ha cerrado la sesión de forma"
    return render_template("frmIniciarSesion.html",mensaje=mensaje)

@app.route("/registrarse/", methods=['GET', 'POST'])
def registrarse():
    try:
        if request.method == 'GET':
            # Obtener la lista de regionales desde la base de datos
            regionales = Regional.objects()
            # Mostrar el formulario de registro con la lista de regionales
            return render_template("frmRegistrarse.html", regionales=regionales)

        elif request.method == 'POST':
            # Procesar los datos enviados desde el formulario
            datos = request.form
            mensaje = None

            # Validar que los datos requeridos estén presentes
            if not all(k in datos for k in ('nombres', 'correo', 'regional', 'usuario', 'password')):
                mensaje = "Todos los campos son obligatorios"
                regionales = Regional.objects()
                return render_template("frmRegistrarse.html", mensaje=mensaje, regionales=regionales)

            # Crear un nuevo instructor
            instructor = Instructor(
                nombres=datos['nombres'],
                correo=datos['correo'],
                regional=datos['regional'],
                usuario=datos['usuario'],
                password=datos['password']
            )
            instructor.save()

            # Redirigir al formulario de inicio de sesión con un mensaje de éxito
            mensaje = "Registro exitoso. Ahora puede iniciar sesión."
            return render_template("frmIniciarSesion.html", mensaje=mensaje)

    except Exception as error:
        mensaje = f"Error al registrar el instructor: {error}"
        regionales = Regional.objects()
        return render_template("frmRegistrarse.html", mensaje=mensaje, regionales=regionales)