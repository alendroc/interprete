from .lexico import AnalisisLexico as lex
from .sintactico import AnalisisSintactico as ans


def compilar(codigo):
    mensaje=[]
    lexico=lex()
    lexico.tokenizar(codigo)
    analisisSintactico=ans(lexico.tokens)
    analisisSintactico.procesarTokens()

    for e in analisisSintactico.errores:
        mensaje.append(e)
        #print(e)

    if len(analisisSintactico.errores)==0:
            mensaje.append("Compilación exitosa")
            #print("Compilación exitosa")
    else: 
        mensaje.append("Error al compilar")
    return "\n".join(mensaje),analisisSintactico


def ejecutar(codigo):
        mensaje,analisisSintac=compilar(codigo)
        resultado=[]
        if not analisisSintac.errores:
            if hasattr(analisisSintac, 'funciones'):
                for funcion in analisisSintac.funciones:
                    nombre_funcion, valor = funcion
                    
                    resultado.append(f"\nFunción: {nombre_funcion}, Valor: {valor}")
        else:
            resultado=mensaje.split("\n")
        
        return "\n".join(resultado)
