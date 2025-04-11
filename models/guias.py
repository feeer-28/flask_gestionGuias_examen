from mongoengine import *
from models.instructor import Instructor

class Guias(Document):
    nombre = StringField(max_length=50, required=True, unique=True)
    descripcion = StringField(max_length=200, required=True)
    programa = StringField(max_length=50, required=True)
    archivo = StringField(required=True)  # Ruta del archivo PDF
    fecha = DateTimeField(required=True)
    instructor = ReferenceField(Instructor, required=True)  # Relación con Instructor

    def __repr__(self):
        return f"{self.nombre} - {self.programa}"
