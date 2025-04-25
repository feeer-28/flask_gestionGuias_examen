from app import app
from flask import render_template, request, session, redirect
from models.instructor import Instructor
from dotenv import load_dotenv
from models.regional import Regional
import os
import yagmail  # Importar yagmail

load_dotenv()

def enviar_correo_registro(instructor, password):
    try:
        # Crear una instancia de yagmail
        yag = yagmail.SMTP(os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
        
        # Asunto y contenido del correo
        subject = 'Bienvenido a la Plataforma de Guías de Aprendizaje SENA'
        contents = f"""
        <h2>Bienvenido {instructor.nombres}</h2>
        <p>Tu registro en la plataforma de Guías de Aprendizaje del SENA ha sido exitoso.</p>
        <p><strong>Tus credenciales de acceso son:</strong></p>
        <ul>
            <li>Correo: {instructor.correo}</li>
            <li>Contraseña: {password}</li>
        </ul>
        <p>Te recomendamos cambiar tu contraseña después de iniciar sesión.</p>
        """
        
        # Enviar el correo
        yag.send(to=instructor.correo, subject=subject, contents=contents)
        print("Correo enviado exitosamente.")
    except Exception as e:
        print(f"Error enviando correo: {str(e)}")

@app.route("/")
def inicio():
    return render_template("frminiciarSesion.html")


@app.route("/iniciarSesion/", methods=['POST'])
def iniciarSesion():
    try:
        mensaje = None
        datos = request.form

        # Validar que los datos requeridos estén presentes
        if 'txtUser' not in datos or 'txtPassword' not in datos:
            mensaje = "Debe ingresar usuario y contraseña"
            return render_template("frminiciarSesion.html", mensaje=mensaje)

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
    return render_template("frminiciarSesion.html", mensaje=mensaje)



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
    return render_template("frminiciarSesion.html",mensaje=mensaje)

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

            # Asegurarse de que la regional seleccionada sea válida
            regional = Regional.objects(id=datos['regional']).first()  # Buscar la regional por ID
            if regional is None:
                mensaje = "Regional no encontrada"
                regionales = Regional.objects()
                return render_template("frmRegistrarse.html", mensaje=mensaje, regionales=regionales)

            # Crear un nuevo instructor
            instructor = Instructor(
                nombres=datos['nombres'],
                correo=datos['correo'],
                regional=regional,  # Guardar la referencia a la región
                usuario=datos['usuario'],
                password=datos['password']
            )
            instructor.save()

            # Enviar correo de bienvenida
            try:
                enviar_correo_registro(instructor, datos['password'])
                mensaje = "Registro exitoso. Se ha enviado un correo de bienvenida."
            except Exception as e:
                mensaje = f"Registro exitoso, pero ocurrió un error al enviar el correo: {e}"

            # Redirigir al formulario de inicio de sesión con un mensaje de éxito
            return render_template("frminiciarSesion.html", mensaje=mensaje)

    except Exception as error:
        mensaje = f"Error al registrar el instructor: {error}"
        regionales = Regional.objects()
        return render_template("frmRegistrarse.html", mensaje=mensaje, regionales=regionales)