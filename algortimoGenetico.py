""" Algoritmo genético problema do caixeiro viajante
"""

from individuo import Individuo
from datetime import datetime
from sklearn.utils import shuffle
import json,requests, random

api_key = "AIzaSyDH4Mf5pA2IsTm8TmzSAjjdohJihq_wOV8"
url = 'https://maps.googleapis.com/maps/api/directions/json?'
"""
GERANDO POPULAÇÃO, FAZENDO REQUEST NA API DO GOOGLE MAPS PARA PEGAR A DISTÂNCIA OS PONTOS PASSADOS
-- USAMOS O GOOGLE MAPS POIS NÃO QUEREMOS UMA DISTÂNCIA EM LINHA RETA
"""


"""montar string waypoints
"""
def montarStringWaypoints(pontos):

    waypoints = ""
    for ponto in range(len(pontos)):
        waypoints += ("via:" if ponto == 0 else "|via:") +pontos[ponto] #coloca o pipe só depois da primeira posição

    return waypoints


"""request api google maps, mostrar tempo e distancia total da viagem
"""
def calculateRoute(origem,pontos):

    """faremos uma requisicao para cada ponto, para acharmos o valor total e o tempo total
    """
    waypoints = montarStringWaypoints(pontos)
    response = requests.get(url +
                            'origin=' + origem +
                            '&destination=' + origem +
                            '&mode=driving&language=pt-BR' +
                            '&waypoints=' + waypoints +
                            '&key=' + api_key)
    return response.json()



"""Gerando População
"""
def geraPopulacaoinicial(origem,pontos):

    populacao = []
    qtdIndividuosInicial = len(pontos)
    print("QUANTIDADE INICIAL DE INDIVIDUOS " + str(qtdIndividuosInicial))

    print(pontos)
    random.shuffle(pontos)
    print(shuffle(pontos))
    #calculo = calculateRoute(origem,pontosEmbaralhado)

    #individuo = Individuo(origem,pontosEmbaralhado,
    #                      calculo["routes"][0]["legs"][0]["duration"]["value"],
    #                      calculo["routes"][0]["legs"][0]["distance"]["value"],
    #                      calculo["routes"][0]["legs"][0]["duration"]["text"],
    #                      calculo["routes"][0]["legs"][0]["distance"]["text"])

    #print(str(individuo))

    return populacao

