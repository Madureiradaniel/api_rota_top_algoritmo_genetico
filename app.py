from flask import Flask, jsonify, request
from flask_restful import Resource, Api
from individuo import *
import os

class home(Resource):
    def get(self):
        nome = request.json['nome']
        return jsonify({"message":"Bem-vindo "+ nome +" ao rota top"})

class calcularRota(Resource):
    def post(self):
        return soma()


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(home, '/api/')
    api.add_resource(calcularRota, '/api/calcularRota/')
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)