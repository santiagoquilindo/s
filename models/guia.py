from mongoengine import Document, StringField, ReferenceField
from models.instructor import Instructor
from models.programasFormacion import Programa
from mongoengine import Document, StringField, DateTimeField

class NombreGuia(Document):
    nombreguia = StringField(max_length=80, required=True)
    descripcions = StringField(max_length=80, required=True)
    programaformacion = StringField(max_length=80, required=True)
    documento = StringField(max_length=200, required=True) 
    fecha = DateTimeField(required=True)
    intructordeproceso = ReferenceField(Instructor, required=True)
    programa = ReferenceField(Programa, required=True)

    def __repr__(self):
        return self.nombreguia