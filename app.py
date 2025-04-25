from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
from mongoengine.connection import get_connection
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__, template_folder=os.path.join(os.getcwd(), 'templates'))
app.secret_key = os.getenv("SECRET_KEY", "1234567890aeiou")
CORS(app)

# Configuración de subida de archivos
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuración de la base de datos MongoDB
mongo_uri = os.environ.get("URI")
if not mongo_uri:
    print("Error: La variable de entorno 'URI' no está configurada.")
    exit(1)

app.config['MONGODB_SETTINGS'] = {
    "db": "GestionGuias",
    "host": mongo_uri
}

# Crear instancia de MongoEngine
db = MongoEngine(app)

# Verificar conexión a MongoDB
with app.app_context():
    try:
        conn = get_connection()
        conn.server_info()  # Esto sí hace una prueba real de conexión
        print("Conexión exitosa a MongoDB")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        exit(1)

# Configuración de yagmail
EMAIL_USER = os.environ.get("MAIL_USERNAME")
EMAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

if not EMAIL_USER or not EMAIL_PASSWORD:
    print("Error: Las variables de entorno 'EMAIL_USER' y 'EMAIL_PASSWORD' no están configuradas.")
    exit(1)

print("Configuración de correo cargada correctamente.")

# Importar rutas
from routes.instructor import *
from routes.guias import *

print("Rutas registradas:")
print(app.url_map)

# Ejecutar la app
if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)
