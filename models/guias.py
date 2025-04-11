from mongoengine import *
from models.instructor import Instructor

# Crear clase que representa la colección Genero en la base de datos
class Guias(Document):
    nombre = StringField(max_length=50, unique=True,required=True)
    descripcion = StringField(max_length=200, required=True)
    programa_formacion = StringField(max_length=50, required=True)
    documento_pdf = FileField(required=True)
    fecha = DateTimeField(required=True)
    instructor = ReferenceField(Instructor,required=True)
    def __repr__(self):
        return self.nombre

