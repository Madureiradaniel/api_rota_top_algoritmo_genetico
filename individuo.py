class Individuo(object):

    def __init__(self,origem,pontos, duracaoTotal, distanciaPercorrerKm, duracaoText,distanciaText ):
        self.pontos = pontos
        self.origem = origem
        self.duracao = duracaoTotal
        self.duracaoText = duracaoText
        self.distancia = distanciaPercorrerKm
        self.distanciaText = distanciaText

    def __str__(self):
        return "Ponto Origem: " + str(self.origem) + "\n" \
               " Duracao Total: " +      str(self.duracaoText) +"\n" + \
               " Distancia Total: " +   str(self.distanciaText) +"\n"  +\
               " Distancia km: " +      str(self.distancia) +"\n"  +\
               " pontos :" +            str(self.pontos)