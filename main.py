from src.sintactico import AnalisisSintactico as sintac
from src.lexico import AnalisisLexico as lex


def main():

    prueba = """num n = (90 + 20 - 10) / 2 * 2:
num n2 = n + n*2:
sim n3 = 'm':
$IMPRIMIR (n2):
"""
    lexic=lex()
    lexic.tokenizar(prueba)
    sintactico=sintac(lexic.tokens)
    sintactico.procesarTokens()
    while sintactico.tokenActual:
        sintactico.declararTipoDato()
        if not sintactico.tokenActual:  # Si no hay más tokens, salir del bucle
            break
    # Código principal del programa
    

if __name__ == "__main__":
    main()

