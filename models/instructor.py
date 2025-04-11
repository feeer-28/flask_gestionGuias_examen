from mongoengine import *

class Instructor(Document):
    usuario = StringField(max_length=50, required=True, unique=True)
    password = StringField(max_length=50,required=True)
    nombres = StringField(max_length=50,required=True)
    regional = StringField(max_length=50,required=True)
    correo = EmailField(required=True, unique=True)
    
    def __repr__(self):
        return f"{self.nombres} {self.regional}"

