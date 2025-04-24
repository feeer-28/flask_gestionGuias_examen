from flask import request, jsonify, render_template, session, redirect, url_for, flash
from werkzeug.utils import secure_filename
from models.instructor import Instructor
from models.guias import Guias
from datetime import datetime
import os
from app import app  # Asegúrate de importar la app desde tu archivo principal
from models.instructor import Instructor

# Ruta API para obtener y subir guías (GET, POST)
@app.route("/api/guias/", methods=['GET', 'POST'])
def api_guias():
    try:
        if request.method == 'GET':
            guias = Guias.objects()
            guias_json = []
            for g in guias:
                guias_json.append({
                    "nombre": g.nombre,
                    "descripcion": g.descripcion,
                    "programa": g.programa,
                    "archivo": g.archivo,
                    "fecha": g.fecha.isoformat(),
                    "instructor": {
                        "nombres": g.instructor.nombres if g.instructor else "Sin instructor",
                        "regional": {
                            "nombre": g.instructor.regional.nombre if g.instructor and g.instructor.regional else "Sin regional"
                        } if g.instructor else None
                    }
                })
            return jsonify({"estado": True, "guias": guias_json}), 200

        elif request.method == 'POST':
            datos = request.form.to_dict()
            archivo = request.files.get('archivo')

            if not archivo or archivo.filename == '':
                return jsonify({"estado": False, "mensaje": "Archivo PDF requerido"}), 400

            filename = secure_filename(archivo.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            archivo.save(filepath)

            instructor_id = session.get('user_id')
            if not instructor_id:
                return jsonify({"estado": False, "mensaje": "Usuario no autenticado"}), 403

            instructor = Instructor.objects(id=instructor_id).first()
            if not instructor:
                return jsonify({"estado": False, "mensaje": "Instructor no encontrado"}), 404

            nueva_guia = Guias(
                nombre=datos['nombre'],
                descripcion=datos['descripcion'],
                programa=datos['programa'],
                archivo=filename,
                fecha=datetime.now(),
                instructor=instructor
            ).save()

            return jsonify({"estado": True, "mensaje": "Guía creada exitosamente"}), 201

    except Exception as error:
        return jsonify({"estado": False, "mensaje": str(error)}), 500


# Ruta para mostrar la lista de guías (vista HTML)
@app.route("/listarGuias/", methods=['GET'])
def listar_guias():
    if "user" not in session:
        flash("Debe iniciar sesión", "warning")
        return redirect(url_for("inicio"))

    # Obtener las guías de la base de datos
    guias = Guias.objects()
    
    # Imprimir guías para depuración
    print(guias)  # Verifica qué datos devuelve la consulta
    
    # Preprocesar las guías para obtener los nombres del instructor y regional
    for guia in guias:
        nombre_instructor = guia.instructor.nombres if guia.instructor else "Sin instructor"
        regional_instructor = guia.instructor.regional.nombre if guia.instructor and guia.instructor.regional else "Sin regional"
        print(f"Nombre del instructor: {nombre_instructor}")
        print(f"Regional del instructor: {regional_instructor}")

    # Renderizar la plantilla con las guías
    return render_template("listarGuias.html", guias=guias)



# Ruta para subir guía desde formulario HTML
@app.route("/subirGuia/", methods=["POST", "GET"])
def subir_guia():
    if "user" not in session:
        flash("Debe iniciar sesión", "warning")
        return redirect(url_for("inicio"))

    if request.method == "POST":
        nombre = request.form.get("nombre")
        descripcion = request.form.get("descripcion")
        programa = request.form.get("programa")
        archivo = request.files["archivo"]

        archivo_path = os.path.join(app.config["UPLOAD_FOLDER"], archivo.filename)
        archivo.save(archivo_path)

        # Buscar el instructor a partir del usuario en sesión
        try:
            instructor = Instructor.objects.get(usuario=session.get("user"))
        except Instructor.DoesNotExist:
            flash("Instructor no encontrado", "danger")
            return redirect(url_for("subir_guia"))

        nueva_guia = Guias(
            nombre=nombre,
            descripcion=descripcion,
            programa=programa,
            archivo=archivo.filename,
            instructor=instructor  # Aquí va el objeto Instructor, no solo el string
        )
        nueva_guia.save()

        flash("Guía subida con éxito", "success")
        return redirect(url_for("listar_guias"))

    return render_template("frmsubirGuia.html")