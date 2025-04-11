from app import app
from flask import request, render_template, redirect, session, url_for, flash
from models.instructor import Instructor
from models.guias import Guias
from datetime import datetime

@app.route("/guias/", methods=['GET'])
def listGuias():
    try:   
        mensaje=None     
        guias= Guias.objects()  
    except Exception as error:
        mensaje=str(error)
    
    return {"mensaje": mensaje, "guias":guias}

@app.route("/guias/", methods=['POST'])
def addGuias():
    try:
        mensaje=None
        estado=False
        if request.method=="POST":
            datos= request.get_json(force=True)           
            instructor= Instructor.objects(id=datos['instructor']).first() 
            if instructor is None:
                mensaje="intructor no existe no se puede crear la guias"
            else: 
                datos['instructor'] = instructor     
                guias = Guias(**datos)
                guias.save()
                estado=True
                mensaje="Guias agregada correctamente" 
        else:
            mensaje="No permitido"   
    except Exception as error:
        mensaje=str(error) 
        mensaje="Ya exsite película con ese código revisar."
        
    return {"estado":estado, "mensaje":mensaje}


@app.route("/guias/", methods=['PUT'])
def updateGuias():
    try:
        mensaje=None
        estado=False
        if request.method=='PUT':
            datos= request.get_json(force=True)
            #obtener Guias por id
            guias = Guias.objects(id=datos['id']).first()
            #actualizar sus atributos
            guias.nombre = datos['nombre']
            guias.descrpcion=datos['descrpcion']
            guias.programa_formacon= datos['programa_formacon']
            guias.documento_pdf = datos['documento_pdf']
            guias.fecha=datos['fecha']
            instructor = Instructor.objects(id=datos['instructor']).first()
            if instructor is None:
                mensaje="No se actualizó el instructor."
            else:
                Guias.instructor=instructor
            Guias.save()
            mensaje = f"{mensaje} Guias Actualizada"
            estado=True            
        else:
            mensaje="No permitido" 
    except Exception as error:
        mensaje=str(error)
        mensaje="No es posible actualizar ya existe."
        
    return {"estado":estado, "mensaje": mensaje}

#vistas

@app.route("/guias/", methods=['GET'])
def listarGuias():
    if ("user" in session):
        guias = Guias.objects()
        instructor = Instructor.objects()
        print(instructor)
        return render_template("listarGuias.html", 
                            guias=guias,
                            instructor=instructor)
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
        


@app.route("/vistaAgregarGuias/", methods=['GET'])
def vistaAgregarGuias():
    if ("user" in session):
        instructor = Instructor.objects()
        return render_template("frmAgregarGuias.html", instructor=instructor)
    else:
        mensaje="Debe primero ingresar con credenciales válidas"
        return render_template("frmIniciarSesion.html", mensaje=mensaje)
        
@app.route("/listarGuias/", methods=["GET"])
def listar_guias():
    if "user" in session:  # Verifica si el usuario ha iniciado sesión
        try:
            # Obtener todas las guías de la base de datos
            guias = Guias.objects()
            return render_template("listarGuias.html", guias=guias)
        except Exception as error:
            flash(f"Error al listar las guías: {error}", "danger")
            return render_template("listarGuias.html", guias=[])
    else:
        flash("Debe iniciar sesión para ver las guías", "warning")
        return redirect(url_for("inicio"))
    
@app.route("/subirGuia/", methods=["GET", "POST"])
def subir_guia():
    if "user" in session:  # Verifica si el usuario ha iniciado sesión
        if request.method == "POST":
            try:
                # Obtener datos del formulario
                nombre = request.form["nombre"]
                descripcion = request.form["descripcion"]
                programa = request.form["programa"]
                archivo = request.files["archivo"]
                instructor_id = session["user_id"]  # ID del instructor en sesión

                # Validar archivo
                if archivo.filename == "":
                    flash("Debe subir un archivo PDF", "warning")
                    return redirect(url_for("subir_guia"))

                # Guardar archivo en el servidor
                archivo_path = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
                archivo.save(archivo_path)

                # Obtener el instructor desde la base de datos
                instructor = Instructor.objects(id=instructor_id).first()
                if not instructor:
                    flash("Instructor no encontrado", "danger")
                    return redirect(url_for("subir_guia"))

                # Crear la guía en la base de datos
                nueva_guia = Guias(
                    nombre=nombre,
                    descripcion=descripcion,
                    programa=programa,
                    archivo=archivo.filename,
                    fecha=datetime.now(),
                    instructor=instructor
                )
                nueva_guia.save()

                flash("Guía subida exitosamente", "success")
                return redirect(url_for("listar_guias"))
            except Exception as e:
                flash(f"Error al subir la guía: {e}", "danger")
                return redirect(url_for("subir_guia"))
        else:
            return render_template("frmSubirGuia.html")
    else:
        flash("Debe iniciar sesión para subir una guía", "warning")
        return redirect(url_for("inicio"))