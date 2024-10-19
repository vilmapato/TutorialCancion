from flask_sqlalchemy import SQLAlchemy 
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
import enum

db = SQLAlchemy()

# create a table for the association many -many between album and canciones
albumes_canciones = db.Table('album_cancion',\
                             db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),\
                                db.Column('cancion_id', db.Integer, db.ForeignKey('cancion.id'), primary_key=True))

# create the classes for each model 

class Cancion(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    minutos = db.Column(db.Integer)
    segundos = db.Column(db.Integer)
    interprete = db.Column(db.String(128))
    #agrego la relacion de una cancion con el album a traves de la table albumes
    albumes = db.relationship('Album', secondary='album_cancion', back_populates='canciones')

    def __repr__(self):
        return "{}-{}-{}-{}".format(self.titulo, self.minutos, self.segundos, self.interprete)
    
class Medio(enum.Enum):
    DISCO = 1
    CASETE = 2
    CD = 3

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    titulo = db.Column(db.String(128))
    anio = db.Column(db.Integer)
    descripcion = db.Column(db.String(512))
    medio = db.Column(db.Enum(Medio))
    usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))
    #relacion con las canciones
    canciones = db.relationship('Cancion', secondary = 'album_cancion', back_populates ='albumes')
    __table_args__ = (db.UniqueConstraint('usuario', 'titulo', name = 'titulo_unico_album'),)

    def __repr__(self):
        return "{}-{}-{}-{}".format(self.titulo, self.anio, self.descripcion, self.medio)
    
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(64))
    contrasena = db.Column(db.String(32))
    albumes = db.relationship('Album', cascade='all, delete, delete-orphan')

#serializacion de los medios a traves de marshmallow para que me arroje el nombre y el valor del medio
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}
    
class AlbumSchema(SQLAlchemyAutoSchema):
    #agrego medio para ser serializado dentro del album
    medio = EnumADiccionario(attribute=('medio'))
    class Meta:
        model = Album
        include_relationships = True
        load_instance = True #que la instacia se cargue cuando accedemos a los esquemas

class CancionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Cancion
        include_relationships = True
        load_instance = True

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Usuario
        include_relationships = True
        load_instance = True