from app import app
from flask import request, render_template, redirect, session
from models.instructor import Instructor
from models.guias import Guias

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
        


