from mongoengine import * 

class Programa(Document):
    nombre =StringField(max_length=80,required=True)
    
    def _repr__(self):
        return self.nombre