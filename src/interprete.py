#from semantico import AnalisisSemantico as sem
from .lexico import AnalisisLexico as lex
from .sintactico import AnalisisSintactico as ans

def compilar(codigo):
    retorno=[]
    lexico=lex()
    lexico.tokenizar(codigo)
    analisisSintactico=ans(lexico.tokens)
    analisisSintactico.procesarTokens()
    while analisisSintactico.tokenActual:
        
        analisisSintactico.declararTipoDato()
        if not analisisSintactico.tokenActual:  # Si no hay más tokens, salir del bucle
            break
    for e in analisisSintactico.errores:
        retorno.append(e)
        #print(e)

    if len(analisisSintactico.errores)==0:
            retorno.append("Compilación exitosa")
            #print("Compilación exitosa")
    else: 
        retorno.append("Error al compilar")
        #print("Error al compilar")
    return retorno