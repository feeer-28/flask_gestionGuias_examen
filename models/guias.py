from mongoengine import *
from datetime import datetime

from app import db
from models.instructor import Instructor  # si tienes referencia a Instructor


class Guias(db.Document):
    nombre = StringField(required=True)
    descripcion = StringField(required=True)
    programa = StringField(required=True)
    archivo = StringField(required=True)  # Nombre del archivo
    fecha = DateTimeField(default=datetime.now)
    instructor = db.ReferenceField('Instructor', required=True)

    meta = {'collection': 'guias'}
