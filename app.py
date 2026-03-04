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

if __name__ == '__main__':
    app.run(debug=True)