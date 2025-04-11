from flask import Flask
from flask_mongoengine import MongoEngine
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = "1234567890aeiou"

# Cors para todas las rutas
CORS(app)

# Configuración de conexión a MongoDB
app.config["UPLOAD_FOLDER"] = "./static/imagenes"
app.config['MONGODB_SETTINGS'] = [{
    "db": "GestionGuias",
    'host': os.environ.get("URI"),
}]

# Crear objeto de tipo MongoEngine
db = MongoEngine(app)

# Verificar conexión a MongoDB dentro del contexto de la aplicación
with app.app_context():
    try:
        db.connection
        print("Conexión exitosa a MongoDB en localhost:27017")
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        exit(1)

# Importar las rutas
from routes.instructor import *
from routes.guias import *

if __name__ == "__main__":
    app.run(port=5000, host="0.0.0.0", debug=True)


