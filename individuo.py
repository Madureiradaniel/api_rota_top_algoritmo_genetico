class Individuo(object):

    fitness = 0

    def __init__(self,origem=None,pontos=None, duracaoTotal=None, distanciaPercorrerKm=None, duracaoText=None,distanciaText=None ):
        self.pontos = pontos
        self.origem = origem
        self.duracao = duracaoTotal
        self.duracaoText = duracaoText
        self.distancia = distanciaPercorrerKm
        self.distanciaText = distanciaText

    def __str__(self):
        return " Ponto Origem: " + str(self.origem) + "\n" \
               " Duracao Total: " +      str(self.duracaoText) +"\n" + \
               " Duracao Segundos: : " + str(self.duracao) + "\n" + \
               " Distancia KM: " +   str(self.distanciaText) +"\n"  +\
               " Distancia: " +      str(self.distancia) +"\n"  +\
               " pontos :" +            str(self.pontos) +"\n"  +\
               " fitness: " + str(self.fitness)