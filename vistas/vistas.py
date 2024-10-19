from flask_restful import Resource
from ..modelos import Cancion, db, CancionSchema
from flask import request

cancion_schema = CancionSchema() #se instancia la cancion_schema para usarla en el api

class VistaCanciones(Resource):

    def get(self):
        return [cancion_schema.dump(cancion) for cancion in Cancion.query.all()]
    
    def post(self): #crear nueva cancion
        nueva_cancion = Cancion(titulo=request.json['titulo'], minutos=request.json['minutos'], segundos=request.json['segundos'], interprete= request.json['interprete'])
        db.session.add(nueva_cancion)
        db.session.commit()
        return [cancion_schema.dump(nueva_cancion)]
    
class VistaCancion(Resource): 

    def get(self, id_cancion): #vista de una cancion con id de cancion
        return [cancion_schema.dump(Cancion.query.get_or_404(id_cancion))]
    
    def put(self, id_cancion): #Update a song so it needs to be populated
        cancion = Cancion.query.get_or_404(id_cancion)
        cancion.titulo = request.json.get('titulo', cancion.titulo) # recibo un diccionario segun python del request y si existe titulo reemplacelo sino no haga nada
        cancion.minutos = request.json.get("minutos",cancion.minutos)
        cancion.segundos = request.json.get("segundos",cancion.segundos)
        cancion.interprete = request.json.get("interprete",cancion.interprete)
        db.session.commit()
        return cancion_schema.dump(cancion)

    def delete(self, id_cancion):
        cancion = Cancion.query.get_or_404(id_cancion)
        db.session.delete(cancion)
        db.session.commit()
        return 'Operacion Exitosa',204