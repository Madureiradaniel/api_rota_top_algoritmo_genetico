from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import os
from algortimoGenetico import *
from flask_cors import CORS


class home(Resource):
    def get(self):
        nome = request.json['nome']
        return jsonify({"message":"Bem-vindo "+ nome +" ao rota top"})

class calcularRota(Resource):
    def post(self):

        qtdGeracoes = 4    # se o melhor for o melhor por mais de N geracoes, o programa para
        countGeracao = 0    # conta a geracao
        countMelhor = 0     # conta a quantidade de vezes que o melhor foi o melhor

        pontos = request.json['pontos']
        origem = request.json['origem']

        if len(pontos) > 7:
             return jsonify({"message:":"A quantidade de pontos ultrapassa o máximo permitido : 7 " })

        populacao = geraPopulacaoinicial(origem, pontos)
        melhor = fitnessFunction(populacao)

        while countMelhor < qtdGeracoes:
            countGeracao += 1
            print("========================================")
            print("GERACAO: " + str(countGeracao))
            print("========================================")
            auxMelhor = melhor

            newPopulacao = crossover(populacao)
            newPopulacao.insert(0, melhor) # insiro o melhor na nova população, o melhor é o modelo
            melhor = fitnessFunction(newPopulacao)
            newPopulacao = mutacao(newPopulacao)
            melhor = fitnessFunction(newPopulacao)

            if melhor == auxMelhor:
                countMelhor += 1
            else:
                countMelhor = 0

        json =jsonify(
                {"origem": origem,
                 "tempo: " : melhor.duracaoText,
                 "Distancia KM: " : melhor.distanciaText,
                 "melhorPontos": melhor.pontos,
                 "Geracao: ": countGeracao})

        return json

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.debug = True
    api = Api(app)
    api.add_resource(home, '/api/')
    api.add_resource(calcularRota, '/api/calcularRota/')
    return app

if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)