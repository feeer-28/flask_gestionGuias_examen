from mongoengine import *
from models.regional import Regional

class Instructor(Document):
    usuario = StringField(max_length=50, required=True, unique=True)
    password = StringField(max_length=50, required=True)
    nombres = StringField(max_length=50, required=True)
    regional = ReferenceField(Regional, required=True)  # Relación con Regional
    correo = EmailField(required=True, unique=True)

    def __repr__(self):
        return f"{self.nombres} ({self.regional.nombre if self.regional else 'Sin regional'})"
