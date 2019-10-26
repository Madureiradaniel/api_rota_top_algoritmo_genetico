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
def calculateRoute (origem,pontos):

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

    print("-----------------------GERANDO POPULAÇÃO-----------------------------------")
    print("QUANTIDADE INICIAL DE INDIVIDUOS " + str(qtdIndividuosInicial))
    print("\n")
    for i in range(qtdIndividuosInicial):

        print("INDIVIDUO: " + str(i+1))
        pontosEmbaralhado = shuffle(pontos)
        calculo = calculateRoute(origem, pontosEmbaralhado)

        individuo = Individuo(origem, pontosEmbaralhado,
                              calculo["routes"][0]["legs"][0]["duration"]["value"],
                              calculo["routes"][0]["legs"][0]["distance"]["value"],
                              calculo["routes"][0]["legs"][0]["duration"]["text"],
                              calculo["routes"][0]["legs"][0]["distance"]["text"])
        populacao.append(individuo)
        print(str(individuo))
        print("________________________________________________________________________")

    return populacao

"""Fitness function
PROBLEMA: ANDAR MENOS NO MENOR TEMPO POSSÍVEL
analogia: quero gastar pouca gasolina e ser o mais rápido possível
"""
def fitnessFunction(populacao):
    #vou decidir quem é o melhor e atribuir uma nota para cada individuo, 0 para pior e 1 para melhor
    print("_______________________FUNCAO_FITNESS_______________________________________\n")

    melhor = populacao[0] #melhor é aquele quem tem o menor tempo e a menor  distancia

    for individuo in populacao[1:]:#escolhendo o melhor
       if (individuo.distancia < melhor.distancia) and (individuo.duracao < melhor.duracao):
           melhor = individuo

    print("MELHOR INDIVIDUO-->" + str(melhor) + "\n")

    count = 1
    for individuo in populacao:#calcular o fitness de acordo com o melhor escolhido
        fitness = ((melhor.distancia/melhor.duracao) / (individuo.distancia/individuo.duracao))
        individuo.fitness = (0 if fitness > 1 else fitness) #caso seja maior do que,1 significa que levou muito tempo, e será punido com 0
        print("INDIVIDUO: "+ str(count)+ " fitness: " + str(individuo.fitness))
        count += 1

    return melhor


"""Método de seleção  
"""
def selecaoRoleta(populacao):

    selecionados = []
    somaPesos = 0
    for individuo in populacao:
        somaPesos += individuo.fitness

    sorteio = random.randint(0, somaPesos)

    #repito o processo do tamanho da minha população
    for i in populacao:
        posicaoEscolhida = -1
        while(sorteio>0):#se sorteio ficar 0 ou negativo achamos nossa posição
            posicaoEscolhida += 1
            sorteio -= populacao[posicaoEscolhida].fitness
        else:
            selecionados.append(populacao[posicaoEscolhida])

    return selecionados #retorno os selecionados, a quantidade vai ser a mesma que a da populacao.

"""Cruzamento(apenas de um ponto)
"""
def crossover(selecionados):
    newPopulacao = []
    return newPopulacao


"""Mutacao (altera um gene)
"""
def mutacao(populacao):
    return 0