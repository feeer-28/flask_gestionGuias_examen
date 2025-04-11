from app import app
from flask import render_template, request, session, redirect,url_for
from models.instructor import Instructor
from dotenv import load_dotenv

load_dotenv()

@app.route("/")
def inicio():
    return render_template("frmIniciarSesion.html")


@app.route("/iniciarSesion/",  methods=['POST'])
def iniciarSesion():
    try:
        mensaje=None
        estado=False
        datos= request.form
        instructor = Instructor.objects(instructor=datos['instructor']).first()
        if instructor is None:
            mensaje="instructor no existe"
        else:
            if instructor.password == datos['password']:
                session["user"] = instructor.instructor
                estado=True
                mensaje="Bienvenido al sistema"
            else:
                mensaje="Contraseña incorrecta" 
    except Exception as error:
        mensaje=str(error) 
        
    return render_template("frminiciarSesion.html", mensaje=mensaje)  


    # Lógica de autenticación (ejemplo básico)
    if username == "admin" and password == "1234":
        return redirect(url_for("home"))  # Redirige a la página principal
    else:
        mensaje = "Usuario o contraseña incorrectos"
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
        return render_template("contenido.html")
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)

@app.route("/salir/")
def exit():
    session.clear()
    mensaje="Ha cerrado la sesión de forma"
    return render_template("frmIniciarSesion.html",mensaje=mensaje)