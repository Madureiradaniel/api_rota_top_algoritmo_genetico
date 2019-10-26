from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
from algortimoGenetico import *


class home(Resource):
    def get(self):
        nome = request.json['nome']
        return jsonify({"message":"Bem-vindo "+ nome +" ao rota top"})

class calcularRota(Resource):
    def post(self):
        pontos = request.json['pontos']
        origem = request.json['origem']

        return jsonify(fitnessFunction(geraPopulacaoinicial(origem,pontos)))

def create_app():
    app = Flask(__name__)
    app.debug = True
    api = Api(app)
    api.add_resource(home, '/api/')
    api.add_resource(calcularRota, '/api/calcularRota/')
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)