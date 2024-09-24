from .semantico import AnalisisSemantico as sem
from .funciones import Funciones as fn
#from lexico import AnalisisLexico as lex
import random

class AnalisisSintactico:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos=0
        self.variables = {}
        self.funciones=[]
        self.errores=[]
        self.linea=1
        self.tokenActual= tokens[0] if tokens else None
        self.analisisSemantico=sem(self.variables,self.linea)
        self.modoCompilacion=False
        
    def consumirToken(self, token):
        if self.tokenActual and self.tokenActual[0] == token:
            self.pos += 1
            if self.pos < len(self.tokens):
                self.tokenActual = self.tokens[self.pos]

            else:
                self.tokenActual = None
        else:
            self.errores.append(f"Error sintáctico: Se esperaba {token}, pero se encontró {self.tokenActual} -> Linea: {self.linea}")
 
           


#DECLARACIONES DE VARIABLES
    def declararTipoDato(self):

        if self.tokenActual[0] in ['NUM', 'SIM', 'CADENA', 'BOOL']:
            self.declaraciones()
        else:
            self.errores.append(f"Error sintáctico: Declaración inesperada, se esperaba un tipo de dato válido -> Linea: {self.linea}")
            self.tokenActual = None

    
    def declaraciones(self):
        tipoDato = self.tokenActual[0]         
        self.consumirToken(tipoDato)

        #VERIFICAR QUE HAYA UN NOMBRE DE VARIABLE
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Token actual es None, se esperaba un nombre de variable.")
            return
        
        #VERIFICAR QUE EL NOMBRE DE VARIABLE NO SE HAYA DECLARADO
        nombreVariable = self.tokenActual[1]
        if nombreVariable in self.variables:
            self.errores.append(f"variable {nombreVariable} ya antes declarada")
            self.tokenActual = None
            return
        
        self.consumirToken('ID')

        #VERIFICAR QUE HAYA UNA ASIGNACIÓN
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Token actual es None, se esperaba asignacion de variable.")
            return
        self.consumirToken('ASIGNAR')

        #VERIFICAR QUE HAYA UN VALOR PARA LA VARIABLE
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Token actual es None, se esperaba un valor.")
            return
        elif tipoDato =="NUM":
            valorExpresion = self.expresionesAritm()
        else:
            valorExpresion=self.analizarVariables()

#VERIFICAR QUE LAS VARIABLES TENGAN EL TIPO DE DATO CORRECTO
        self.analisisSemantico.linea=self.linea
        validar,error=self.analisisSemantico.verificarCompatibilidad(tipoDato,valorExpresion)

        if validar:
            self.variables[nombreVariable] = valorExpresion
            if self.modoCompilacion:
                print(f"Declaración de {tipoDato} {nombreVariable} = {valorExpresion}")
        else:
            self.errores.append(error)

        if self.tokenActual and self.tokenActual[0] == 'FIN_LINEA':
            self.consumirToken('FIN_LINEA')
            self.linea+=1
        else:
            self.errores.append(f"Error sintáctico: Se esperaba FIN_LINEA = ':' pero se encontró {self.tokenActual} -> Linea: {self.linea}")
       
      


#EXPRESIONES ARITMETICAS PARA ASIGNAR NUMEROS
    def expresionesAritm(self):
        result = self.multiplicacionDivision()
        
        while self.tokenActual and self.tokenActual[0] in ['SUMA', 'RESTA']:
            token = self.tokenActual
            if token[0] == 'SUMA':
                self.consumirToken('SUMA')
                siguienteValor = self.multiplicacionDivision()
                validar, error = self.analisisSemantico.verificarNumero(siguienteValor)
                if not validar:
                    self.errores.append(error)
                    return None
                result += siguienteValor
            elif token[0] == 'RESTA':
                self.consumirToken('RESTA')
                siguienteValor = self.multiplicacionDivision()
                validar, error = self.analisisSemantico.verificarNumero(siguienteValor)
                if not validar:
                    self.errores.append(error)
                    return None
                result -= siguienteValor
        return result

    def multiplicacionDivision(self):
        result = self.asignarParentesis()
        
        while self.tokenActual and self.tokenActual[0] in ['MULT', 'DIV']:
            token = self.tokenActual
            if token[0] == 'MULT':
                self.consumirToken('MULT')
                siguienteValor = self.asignarParentesis()
                validar, error = self.analisisSemantico.verificarNumero(siguienteValor)
                if not validar:
                    self.errores.append(error)
                    return None
                result *= siguienteValor

            elif token[0] == 'DIV':
                self.consumirToken('DIV')
                siguienteValor = self.asignarParentesis()
                validar, error = self.analisisSemantico.verificarNumero(siguienteValor)
                if not validar:
                    self.errores.append(error)
                    return None
                result /= siguienteValor
        return result
    

    def asignarParentesis(self):
            if self.tokenActual[0] == 'PARENTESIS_I':
                self.consumirToken('PARENTESIS_I')
                result = self.expresionesAritm()
                self.consumirToken('PARENTESIS_D')
                return result
            return self.analizarVariables()
    
#FIN DE ASIGNACION DE NUMEROS

#DEVUELVE EL VALOR DE LA VARIABLE
    def analizarVariables(self):
        self.analisisSemantico.linea=self.linea
        token = self.tokenActual
        if token[0] == 'NUMERO':
            self.consumirToken('NUMERO')
            return float(token[1])
        elif token[0] == 'TEXTO':
            self.consumirToken('TEXTO')
            return str(token[1])
        elif token[0] == 'CAR':
            self.consumirToken('CAR')
            return token[1][1]
        elif token[0] == 'VERDADERO':
            self.consumirToken('VERDADERO')
            return True
        elif token[0] == 'FALSO':
            self.consumirToken('FALSO')
            return False
        elif token[0] == 'ID':
            nombreVariable = token[1]
            self.consumirToken('ID')
            validar, error=self.analisisSemantico.verificarDeclaracion(nombreVariable)
            if not validar:
                self.errores.append(error)
                return None
            return self.variables[nombreVariable]
        else:
            self.errores.append(f'Token inesperado al asignar valor -> Linea: {self.linea}')
            return None
    


    def sintaxis_Funcion_Imprimir(self):
         self.consumirToken('LLAMAR_IMPRIMIR')
         self.consumirToken('PARENTESIS_I')
         ID =self.tokenActual[1]
         self.consumirToken('ID')
         self.consumirToken('PARENTESIS_D')
         self.consumirToken('FIN_LINEA')
         if ID in self.variables:
          valor = self.variables[ID]
          print(f"Salida-> {valor}")

    def sintaxis_funcion_Numero_Aleatorio(self):
        self.consumirToken('LLAMAR_NUM_ALEATORIO')
        self.consumirToken('PARENTESIS_I')
        # if self.tokenActual[0]=='NUMERO'
        rangoInicial = self.analizarVariables()
       # self.consumirToken('NUMERO')
        self.consumirToken('SEPARADOR')  
        rangoFinal = self.analizarVariables() 
        #self.consumirToken('NUMERO')
        self.consumirToken('PARENTESIS_D')  
        self.consumirToken('FIN_LINEA')

        validacion,error=self.analisisSemantico.verificarNumero(rangoInicial)
        if not validacion: self.errores.append(error)
        validacion,error=self.analisisSemantico.verificarNumero(rangoFinal)
        if not validacion: self.errores.append(error)

        self.funciones.append(('numeroAleatorio',fn.numeroAleatorio(rangoInicial,rangoFinal)))
    

    def definirFuncion(self):
       if self.tokenActual[0] == 'LLAMAR_IMPRIMIR':
          self.sintaxis_Funcion_Imprimir()

       elif self.tokenActual[0] == 'LLAMAR_NUM_ALEATORIO':
           self.sintaxis_funcion_Numero_Aleatorio()

       #elif FUNCION OPTENER FECHA ACTUAL, DANIEL
       else:
            print(f"Error sintáctico: Comando inesperado {self.tokenActual}")

    def procesarTokens(self):
     while self.tokenActual:

        if self.tokenActual[0] in ['LLAMAR_IMPRIMIR', 'LLAMAR_NUM_ALEATORIO']:
           self.definirFuncion()
        else:
           self.declararTipoDato()
        

    def limpiarEstado(self):
        self.funciones.clear()
        self.errores.clear()
        self.tokenActual = None
        self.pos=0

#FIN DECLARACIONES DE VARIABLES
