# from src.sintactico import AnalisisSintactico as sintac
# from src.lexico import AnalisisLexico as lex
from src.interpreterView import InterpreterView



def main():

#     prueba = """num n = (90 + 20 - 10) / 2 * 2:
# num n2 = n + n*2:
# sim n3 = 'm':
# $IMPRIMIR (n2):
# """
    vista=InterpreterView()
    #codigo=compilar(vista.codeTxt.get())
    vista.onCompileEvent()
    
    

if __name__ == "__main__":
    main()


