""" Algoritmo genético problema do caixeiro viajante
"""

from individuo import Individuo
from datetime import datetime
from random import randint,uniform
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
    qtdIndividuosInicial = len(pontos)*2 # a quantidade de individuos vai depender da quantidade de pontos

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
    for individuo in populacao: # calcular o fitness de acordo com o melhor escolhido
        fitness = ((melhor.distancia/melhor.duracao) / (individuo.distancia/individuo.duracao))
        individuo.fitness = (0 if fitness > 1 else fitness) # caso seja maior do que,1 significa que levou muito tempo, e será punido com 0
        print("INDIVIDUO: "+ str(count)+ " fitness: " + str(individuo.fitness))
        count += 1

    return melhor


"""Método de seleção  
"""
def selecaoRoleta(populacao):
    #print("_________________SELECAO____________________________\n")

    selecionado = []
    somaPesos = 0

    for individuo in populacao:
        somaPesos += individuo.fitness

    sorteio = uniform(0, somaPesos)
    posicaoEscolhida = -1

    while sorteio > 0: #se sorteio ficar 0 ou negativo achamos nossa posição
        posicaoEscolhida += 1
        sorteio -= populacao[posicaoEscolhida].fitness
    else:
        selecionado = populacao[posicaoEscolhida]

    #print("_________________INDIVIDUO SELECIONADO____________________________\n")
    #print(str(selecionado) + "\n")

    return selecionado #retorno os selecionados, a quantidade vai ser a mesma que a da populacao.

"""Cruzamento(Cruzamento ordenado pois os pontos não pode se repetir)
"""
def crossover(populacao):

    print("_________________CROSSOVER____________________________\n")

    newPopulacao = []

    for i in populacao: #vou gerar a mesma quantidade de individuos  para a nova geracao

        filho = Individuo()
        filhoParte1 = []
        pai1 = selecaoRoleta(populacao)
        pai2 = selecaoRoleta(populacao)

        #escolho os genes inicial e final para pegarmos do pai1
        gene1 = int(randint(0,len(pai1.pontos)))
        gene2 = int(randint(0, len(pai1.pontos)))

        menor = min(gene1,gene2)
        maior = max(gene1,gene2)

        #print("maior " + str(maior) + "menor " + str(menor))
        for i in range(menor,maior):
            filhoParte1.append(pai1.pontos[i])

        filhoParte2 = [ponto for ponto in pai2.pontos if ponto not in filhoParte1] #pega os pontos restantes que não estão na parte 1

        filho.pontos = filhoParte1 + filhoParte2 #junta as duas partes para formar uma só

        calculo = calculateRoute(pai1.origem, filho.pontos)

        filho.origem = pai1.origem
        filho.duracao = calculo["routes"][0]["legs"][0]["duration"]["value"]
        filho.distancia = calculo["routes"][0]["legs"][0]["distance"]["value"]
        filho.duracaoText = calculo["routes"][0]["legs"][0]["duration"]["text"]
        filho.distanciaText = calculo["routes"][0]["legs"][0]["distance"]["text"]
        newPopulacao.append(filho)

        print("_________________NOVO INDIVIDUO____________________________\n")
        print(str(filho))

    return newPopulacao


"""Mutacao (altera um gene)
"""
def mutacao(populacao):
    print("_________________MUTACAO____________________________\n")
    menor = 0 #meu criterio para mutação é pegar quem tem o menor fitness
    for individuo in range(len(populacao[1:])):
        if populacao[individuo].fitness < populacao[menor].fitness:
            menor = individuo

    # escolho dois pontos aleatorios para fazer a troca no individuo
    ponto1 = randint(0, len(populacao[menor].pontos)-1)
    ponto2 = randint(0, len(populacao[menor].pontos)-1)

    while ponto1 == ponto2:
        ponto2 = randint(0, len(populacao[menor].pontos)-1)

    print("pontos antes: " + str(populacao[menor].pontos))
    aux = populacao[menor].pontos[ponto1]
    populacao[menor].pontos[ponto1] = populacao[menor].pontos[ponto2]
    populacao[menor].pontos[ponto2] = aux
    print("pontos depois: " + str(populacao[menor].pontos))

    #com os pontos trocados novamente chamo a api para calcular o KM e o TEMPO

    calculo = calculateRoute(populacao[menor].origem,populacao[menor].pontos)
    populacao[menor].duracao = calculo["routes"][0]["legs"][0]["duration"]["value"]
    populacao[menor].distancia = calculo["routes"][0]["legs"][0]["distance"]["value"]
    populacao[menor].duracaoText = calculo["routes"][0]["legs"][0]["duration"]["text"]
    populacao[menor].distanciaText = calculo["routes"][0]["legs"][0]["distance"]["text"]

    return populacao