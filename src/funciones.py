import random

class Funciones:

    @staticmethod
    def numeroAleatorio(rangoInicio, rangoFinal):
        return random.randint(int(rangoInicio), int(rangoFinal))

    # @staticmethod
    # def imprimir(valor):
    #     print(f"Salida: {valor}")
