from flaskr import create_app
from flask_restful import Api
from .modelos import db, Cancion, Album, Usuario, Medio
from .modelos import AlbumSchema, UsuarioSchema, CancionSchema
from .vistas import VistaCancion, VistaCanciones

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

# Prueba de los modelos
""" with app.app_context():
    c = Cancion(titulo = 'Prueba', minutos=2, segundos = 25, interprete = 'Vilma')
    c1 = Album(titulo = 'exitos', anio = 1990, descripcion = 'primer album', medio = Medio.CD)
    u = Usuario(nombre = 'Pato', contrasena = '12345')
    u.albumes.append(c1)
    c1.canciones.append(c)
    db.session.add(u)
    db.session.add(c)
    db.session.add(c1)
    db.session.commit()
    print(Album.query.all())
    print(Album.query.all()[0].canciones)
    print(Cancion.query.all())
    db.session.delete(c1) # prueba si despues de eliminar usuario/cancion se elimina el album
    print(Cancion.query.all())
    print(Album.query.all()) """

#prueba de serializaciones
""" with app.app_context():
    album_schema = AlbumSchema()
    cancion_schema = CancionSchema()
    c1 = Album(titulo = 'exitos', anio = 1990, descripcion = 'primer album', medio = Medio.CD)
    c = Cancion(titulo = 'Prueba', minutos=2, segundos = 25, interprete = 'Vilma')
    db.session.add(c)
    db.session.add(c1)
    db.session.commit()
    #se hace el print de todos los albums en formato json com dumps
    print([album_schema.dumps(Cancion) for Cancion in Cancion.query.all()]) """

api = Api(app)
api.add_resource(VistaCanciones, '/canciones')
api.add_resource(VistaCancion, '/cancion/<int:id_cancion>')