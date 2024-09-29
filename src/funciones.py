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
        return valor
    
    #3-OBTENER FECHA ACTUAL
    @staticmethod
    def fechaActual():
        return date.today()
    
    #4-CONTAR VOCALES DE UNA CADENA
    @staticmethod
    def contarVocales(texto):
        vocales="AEIOUaeiou"
        return sum(1 for v in texto if v in vocales)

    #5-POTENCIA DE NUMERO
    @staticmethod
    def potencia(base, exponente):
        return base ** exponente
    

    #6-MOSTRAR LONGITUD DE CADENA
    @staticmethod
    def longitudTexto(texto):
        return len(texto)-2
    
    #7-CONCATENAR CADENAS
    @staticmethod
    def concatenarTexto(texto1, texto2):
        return str(texto1).strip('"')+str(texto2).strip('"')
    
    #8-MOSTRAR SINTAXIS DE FUNCIONES
    @staticmethod
    def mostrarSintaxisFunc():
        return (
    """\t----DECLARACION DE FUNCIONES-----
    \nOBTENER NUMERO ALEATORIO          ----> $ALEATORIO(1,100):
    \nIMPRIMIR CUALQUIER VALOR          ----> $IMPRIMIR("Interprete Yakuza"):
    \nOBTENER FECHA ACTUAL              ----> $OBTENER_FECHA():
    \nCONTAR VOCALES DE UNA CADENA      ----> $CONT_VOCALES("Este es el proyecto de paradigmas"):
    \nPOTENCIA DE NUMERO                ----> $POTENCIA(2,4):
    \nMOSTRAR LONGITUD DE CADENA        ----> $LONGITUD("Paradigmas de programacion"):
    \nCONCATENAR CADENAS                ----> $CONCATENAR("Hola ","mundo"):
    \nMOSTRAR SINTAXIS DE FUNCIONES     ----> $FUNCIONES():
    \nMOSTRAR SINTAXIS DE DECLARACIONES ----> $DECLARACIONES():
    \nVALIDAR NUMERO PAR                ----> $PAR(2):
    \nCONVERTIR TEXTO A MINUSCULA       ----> $MINUS("CONVIERTE ESTO EN MINUSCULA"):
    \nCONVERTIR TEXTO A MAYUSCULA       ----> $MAYUS("convierte esto en mayuscula"):
    \nOBTENER SUBCADENA DE TEXTO        ----> $SUBCADENA("obtiene subcadena",2,9):
"""
        )


    #9-MOSTRAR SINTAXIS DE DECLARACIONES
    @staticmethod
    def mostrarSintaxisDecl():
        return (
    """\t----DECLARACION DE VARIABLES-----
    \n'num': Declaración de numerico ----> num n1 = 4:
    \n'sim': Declaración de char     ----> sim n2 = 'b':
    \n'bool': Declaración de booleano----> bool n3 = verdadero/falso || 1/0:
    \n'cadena': Declaración de string----> cadena n4 = "hola mundo":
"""
        )
    
    #10-DEMUESTRA SI EL NUMERO ES PAR
    @staticmethod
    def esPar(numero):
        return True if numero%2==0 else False
    
    #11-CONVERTIR TEXTO A MINUSCULA
    @staticmethod
    def convertirMinus(texto):
        return str.lower(texto)
    
    #12-CONVERTIR TEXTO A MAYUSCULA
    @staticmethod
    def convertirMayus(texto):
        return str.upper(texto)
    
    #13-OBTENER SUBCADENA
    @staticmethod
    def obtenerSubCadena(texto,rangoInicio,rangoFinal):
        return texto[rangoInicio:rangoFinal]
    

    