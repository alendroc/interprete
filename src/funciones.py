import random
from datetime import date
class Funciones:

    # 1-OBTENER NUMERO ALEATORIO
    @staticmethod
    def numeroAleatorio(rangoInicio, rangoFinal):
        return random.randint(int(rangoInicio), int(rangoFinal))
    
    #2-IMPRIMIR CUALQUIER VALOR
    @staticmethod
    def imprimir(valor):
        print(valor)
    
    #3-OBTENER FECHA ACTUAL
    @staticmethod
    def fechaActual():
        return date.today()

    #3-CONCATENAR CADENAS ALE
    
    #5-CONTAR VOCALES DE UNA CADENA JOSUE
    #6-POTENCIA DE NUMERO JOSUE
    #7-MOSTRAR SINTAXIS DE FUNCIONES JOSUE
    #8-MOSTRAR SINTAXIS DE DECLARACIONES JOSUE
    #9-MOSTRAR LONGITUD DE CADENA