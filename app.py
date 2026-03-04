import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv 

#Cargar las variables de entorno
load_dotenv()

#crear instancia
app =  Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#Modelo de la base de datos
class Comidas(db.Model):
    __tablename__ = 'comidas'
    id_comida = db.Column(db.String, primary_key=True)
    nombre = db.Column(db.String)
    precio = db.Column(db.String)

#endpoint para obtener todas las comidas
@app.route('/comidas', methods=['GET'])
def get_comidas():
    comidas = Comidas.query.all()
    lista_comidas = []
    for comida in comidas:
        lista_comidas.append({
            'id_comida': comida.id_comida,
            'nombre': comida.nombre,
            'precio': comida.precio,
        })
    return jsonify(lista_comidas)

#endpoint para obtener una comida por el id_comida
@app.route('/comidas/<id_comida>', methods=['GET'])
def get_comida(id_comida):
    comida = Comidas.query.get(id_comida)
    if comida is None:
        return jsonify({'msj': 'Comida no encontrada'})
    return jsonify({
        'id_comida': comida.id_comida,
        'nombre': comida.nombre,
        'precio': comida.precio,
    })

#endpoint para eliminar una comida por el id_comida
@app.route('/comidas/<id_comida>', methods=['DELETE'])
def delete_comida(id_comida):
    comida = Comidas.query.get(id_comida)
    if comida is None:
        return jsonify({'msj': 'Comida no encontrada'})
    db.session.delete(comida)
    db.session.commit()
    return jsonify({'msj': 'Comida eliminada correctamente'})

#endpoint para agregar una nueva comida
@app.route('/comidas', methods=['POST'])
def insert_comida():
    data = request.get_json()
    nueva_comida = Comidas(
        id_comida=data['id_comida'],
        nombre=data['nombre'],
        precio=data['precio'],
    )
    db.session.add(nueva_comida)
    db.session.commit()
    return jsonify({'msg': 'Comida agregada correctamente'})

#endpoint para actualizar una comida por el id_comida
@app.route('/comidas/<id_comida>', methods=['PUT'])
def update_comida(id_comida):
    comida = Comidas.query.get(id_comida)
    if comida is None:
        return jsonify({'msj': 'Comida no encontrada'})
    data = request.get_json()
    if 'nombre' in data:
        comida.nombre = data['nombre']
    if 'precio' in data:
        comida.precio = data['precio']
    db.session.commit()
    return jsonify({'msj': 'Comida actualizada correctamente'})

if __name__ == '__main__':
    app.run(debug=True)