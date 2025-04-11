from mongoengine import Document, StringField

class Regional(Document):
    nombre = StringField(max_length=50, required=True, unique=True)

    def __repr__(self):
        return self.nombre