from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
from mongoengine.connection import get_connection  # <- Importación clave
import os


# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
app.secret_key = os.getenv("SECRET_KEY", "1234567890aeiou")
CORS(app)

# Configuración
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER




mongo_uri = os.environ.get("URI")
print(f" URI cargada: {mongo_uri}")

app.config['MONGODB_SETTINGS'] = {
    "db": "GestionGuias",
    "host": mongo_uri
}

# Crear instancia de MongoEngine
db = MongoEngine(app)

# Verificar conexión
with app.app_context():
    try:
        conn = get_connection()
        conn.server_info()  # Esto sí hace una prueba real de conexión
        print(" Conexión exitosa a MongoDB")
    except Exception as e:
        print(f" Error al conectar a MongoDB: {e}")
        exit(1)

# Importar rutas
from routes.instructor import *
from routes.guias import *

print("Rutas registradas:")
print(app.url_map)


# Ejecutar la app
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
