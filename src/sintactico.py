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
        #USAR NUMEROS NEGATIVOS
        negativo = False
        if self.tokenActual and self.tokenActual[0] == 'RESTA':
            self.consumirToken('RESTA')
            negativo = True
        
        result = self.multiplicacionDivision()
        
        if negativo:
            result = -result
        
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
    

# SINTAXIS DE FUNCIONES PARA OPTIMIZAR
    def parentesisIzq(self):
      if self.tokenActual is None or self.tokenActual[0] != 'PARENTESIS_I':
            self.errores.append("Error sintáctico: Se esperaba 'PARENTESIS_I'")
            return
      self.consumirToken('PARENTESIS_I')
     
    def parentesisDer(self):
      if self.tokenActual is None or self.tokenActual[0] != 'PARENTESIS_D':
            self.errores.append("Error sintáctico: Se esperaba 'PARENTESIS_D'")
            return
      self.consumirToken('PARENTESIS_D')

    def dosPuntosFinal(self):
        if self.tokenActual is None or self.tokenActual[0] != 'FIN_LINEA':
            self.errores.append("Error sintáctico: Se esperaba 'FIN_LINEA'")
            return  
        self.consumirToken('FIN_LINEA')

    def coma(self):
        if self.tokenActual is None or self.tokenActual[0] != 'SEPARADOR':
            self.errores.append("Error sintáctico: Se esperaba un 'SEPARADOR'")
            return
        self.consumirToken('SEPARADOR')
#fin de recursos para una funcion

#Funciones del sistema-----------------------------
#OBTENER NUMERO ALEATORIO DE UN RANGO DADO
    def sintaxisFuncionNumeroAleatorio(self):
        self.consumirToken('LLAMAR_NUM_ALEATORIO')
        self.parentesisIzq()

        if self.tokenActual is None :
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO'")
            return
        rangoInicial = self.expresionesAritm()
        validacion, error = self.analisisSemantico.verificarNumero(rangoInicial)
        if not validacion:
            self.errores.append(f"Rango inicial inválido: {error}")
            return
        
        self.coma()

        if self.tokenActual is None :
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO'")
            return
        rangoFinal = self.expresionesAritm()
        validacion, error = self.analisisSemantico.verificarNumero(rangoFinal)
        if not validacion:
            self.errores.append(f"Rango final inválido: {error}")
            return
        
        self.parentesisDer()
        self.dosPuntosFinal()

        if rangoFinal < rangoInicial:
            self.errores.append(f"Error semántico: El rango final ({rangoFinal}) no puede ser menor que el rango inicial ({rangoInicial}).\n")
            return 
        if not self.errores:
            self.funciones.append(('numeroAleatorio',fn.numeroAleatorio(rangoInicial,rangoFinal)))

#IMPRIME EL VALOR QUE SE PONGA O VARIABLES DEFINIDAS
    def sintaxisFuncionImprimir(self):
        self.consumirToken('LLAMAR_IMPRIMIR')
        self.parentesisIzq()

        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para imprimir.")
            return
        valor=self.expresionesAritm()
        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('imprimir',fn.imprimir(valor)))


#OBTENER FECHA ACTUAL
    def sintaxisFuncionObtenerFechaActual(self):
        self.consumirToken('LLAMAR_OBTENER_FECHA_ACTUAL')
        self.parentesisIzq()
        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('FechaActual',fn.fechaActual()))

#OBTENER SINTAXIS DE LAS DECLARACIONES DE VARIABLES
    def sintaxisFuncionObtenerDeclaraciones(self):
        self.consumirToken('LLAMAR_SINTAXIS_DECLARACIONES')
        self.parentesisIzq()
        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('declaracionesVariables',fn.mostrarSintaxisDecl()))

#OBTENER SINTAXIS DE LAS DECLARACIONES DE FUNCIONES
    def sintaxisFuncionObtenerFunciones(self):
        self.consumirToken('LLAMAR_SINTAXIS_FUNCIONES')
        self.parentesisIzq()
        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('funcionesLocales',fn.mostrarSintaxisFunc()))

#OBTENER LA CANTIDAD DE VOCALES DE UN TEXTO
    def sintaxisFuncionContarVocales(self):
        self.consumirToken('LLAMAR_CONTAR_VOCALES')
        self.parentesisIzq()
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para contar vocales.")
            return
        
        valor=self.analizarVariables()
        validar,error=self.analisisSemantico.verificarCadena(valor)
        if not validar:
            self.errores.append(error)
            return

        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('contarVocales',fn.contarVocales(valor)))

#OBTENER POTENCIA DE UN NUMERO
    def sintaxisFuncionPotencia(self):
        self.consumirToken('LLAMAR_POTENCIA')
        self.parentesisIzq()

        if self.tokenActual is None :
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO'")
            return
        numBase = self.expresionesAritm()
        validacion, error = self.analisisSemantico.verificarNumero(numBase)
        if not validacion:
            self.errores.append(error)
            return
        
        self.coma()

        if self.tokenActual is None :
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO'")
            return
        numPow = self.expresionesAritm()
        validacion, error = self.analisisSemantico.verificarNumero(numPow)
        if not validacion:
            self.errores.append(error)
            return
        
        self.parentesisDer()
        self.dosPuntosFinal()

        if not self.errores:
            self.funciones.append(('potenciaNumero',fn.potencia(numBase,numPow)))

#OBTENER LA LONGITUD DE UN TEXTO
    def sintaxisFuncionLongitudCadena(self):
        self.consumirToken('LLAMAR_LONGITUD_CADENA')
        self.parentesisIzq()

        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para extraer la longitud de la cadena.")
            return
        
        valor=self.analizarVariables()
        validar,error=self.analisisSemantico.verificarCadena(valor)
        if not validar:
            self.errores.append(error)
            return

        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('extraerLongitud',fn.longitudTexto(valor)))

#CONCATENAR 2 CADENAS
    def sintaxisFuncionConcatenarCadenas(self):
        self.consumirToken('LLAMAR_SINTAXIS_CONCATENAR_CADENAS')
        self.parentesisIzq()
        
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para la cadena.")
            return
        
        valor1=self.analizarVariables()
        validar,error=self.analisisSemantico.verificarCadena(valor1)
        if not validar:
            self.errores.append(error)
            return
        
        self.coma()

        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para la cadena.")
            return
        
        valor2=self.analizarVariables()
        validar,error=self.analisisSemantico.verificarCadena(valor2)
        if not validar:
            self.errores.append(error)
            return


        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('concatenarCadenas',fn.concatenarTexto(valor1,valor2)))

#VERIFICAR SI UN NUMERO ES PAR
    def sintaxisFuncionVerificarNumeroPar(self):
        self.consumirToken('LLAMAR_SINTAXIS_ES_PAR')
        self.parentesisIzq()

        if self.tokenActual is None :
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO'")
            return
        numBase = self.expresionesAritm()
        validacion, error = self.analisisSemantico.verificarNumero(numBase)
        if not validacion:
            self.errores.append(error)
            return
        
        self.parentesisDer()
        self.dosPuntosFinal()

        if not self.errores:
            self.funciones.append(('numeroPar',fn.esPar(numBase)))

#CONVERTIR CADENA A MINUSCULA
    def sintaxisFuncionConvertirMinus(self):
        self.consumirToken('LLAMAR_SINTAXIS_CADENA_MINUSCULA')
        self.parentesisIzq()
        
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para la cadena.")
            return
        
        valor1=self.analizarVariables()
        validar,error=self.analisisSemantico.verificarCadena(valor1)
        if not validar:
            self.errores.append(error)
            return


        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('convertirMinuscula',fn.convertirMinus(valor1)))


#CONVERTIR CADENA A MAYUSCULA
    def sintaxisFuncionConvertirMayus(self):
        self.consumirToken('LLAMAR_SINTAXIS_CADENA_MAYUSCULA')
        self.parentesisIzq()
        
        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para la cadena.")
            return
        
        valor1=self.analizarVariables()
        validar,error=self.analisisSemantico.verificarCadena(valor1)
        if not validar:
            self.errores.append(error)
            return


        self.parentesisDer()
        self.dosPuntosFinal()
        self.funciones.append(('convertirMayuscula',fn.convertirMayus(valor1)))


#OBTENER SUBCADENA DE CADENA POR RANGOS DE INDICES
    def sintaxisFuncionObtenerSubcadena(self):
        self.consumirToken('LLAMAR_SINTAXIS_OBTENER_SUBCADENA')
        self.parentesisIzq()

        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba un valor para la cadena.")
            return

        texto = self.analizarVariables()
        validar, error = self.analisisSemantico.verificarCadena(texto)
        if not validar:
            self.errores.append(error)
            return

        self.coma()

        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO' para el rango inicial.")
            return
        rangoInicio = self.expresionesAritm()
        if rangoInicio is None:
            self.errores.append("Error semántico: Se esperaba un número para el rango inicial, pero no se proporcionó.")
            return

        try:
            rangoInicio = int(rangoInicio)
            validacion, error = self.analisisSemantico.verificarNumero(rangoInicio)
            if not validacion:
                self.errores.append(error)
                return
        except ValueError:
            self.errores.append(f"Error semántico: Se esperaba un número entero para el rango inicial, pero se encontró '{rangoInicio}'.")
            return

        self.coma()

        if self.tokenActual is None:
            self.errores.append("Error sintáctico: Se esperaba 'NUMERO' para el rango final.")
            return
        rangoFinal = self.expresionesAritm()
        if rangoFinal is None:
            self.errores.append("Error semántico: Se esperaba un número para el rango final, pero no se proporcionó.")
            return

        try:
            rangoFinal = int(rangoFinal)
            validacion, error = self.analisisSemantico.verificarNumero(rangoFinal)
            if not validacion:
                self.errores.append(error)
                return
        except ValueError:
            self.errores.append(f"Error semántico: Se esperaba un número entero para el rango final, pero se encontró '{rangoFinal}'.")
            return

        self.parentesisDer()
        self.dosPuntosFinal()

        if rangoInicio < 0 or rangoFinal > len(texto):
            self.errores.append(f"Error semántico: Los rangos deben estar entre 0 y {len(texto)}.")
            return
        if  rangoInicio>rangoFinal:
            self.errores.append(f"Error semántico: El rango final debe ser mayor a {rangoInicio}")
            return

        self.funciones.append(('obtenerSubcadena', fn.obtenerSubCadena(texto, rangoInicio, rangoFinal)))

#-----

    def definirFuncion(self):
       if self.tokenActual[0] == 'LLAMAR_IMPRIMIR':
          self.sintaxisFuncionImprimir()
       elif self.tokenActual[0] == 'LLAMAR_NUM_ALEATORIO':
           self.sintaxisFuncionNumeroAleatorio()
       elif self.tokenActual[0] == 'LLAMAR_OBTENER_FECHA_ACTUAL':
            self.sintaxisFuncionObtenerFechaActual()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_DECLARACIONES':
           self.sintaxisFuncionObtenerDeclaraciones()
       elif self.tokenActual[0]=='LLAMAR_CONTAR_VOCALES':
           self.sintaxisFuncionContarVocales()
       elif self.tokenActual[0]=='LLAMAR_POTENCIA':
           self.sintaxisFuncionPotencia()
       elif self.tokenActual[0]=='LLAMAR_LONGITUD_CADENA':
           self.sintaxisFuncionLongitudCadena()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_CONCATENAR_CADENAS':
           self.sintaxisFuncionConcatenarCadenas()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_FUNCIONES':
           self.sintaxisFuncionObtenerFunciones()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_ES_PAR':
           self.sintaxisFuncionVerificarNumeroPar()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_CADENA_MINUSCULA':
           self.sintaxisFuncionConvertirMinus()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_CADENA_MAYUSCULA':
           self.sintaxisFuncionConvertirMayus()
       elif self.tokenActual[0]=='LLAMAR_SINTAXIS_OBTENER_SUBCADENA':
           self.sintaxisFuncionObtenerSubcadena()
       else:
            print(f"Error sintáctico: Comando inesperado {self.tokenActual}")

    def procesarTokens(self):
     while self.tokenActual:
        if self.tokenActual[0] in ['LLAMAR_IMPRIMIR', 'LLAMAR_NUM_ALEATORIO','LLAMAR_OBTENER_FECHA_ACTUAL',
                                   'LLAMAR_SINTAXIS_DECLARACIONES','LLAMAR_CONTAR_VOCALES','LLAMAR_POTENCIA',
                                   'LLAMAR_LONGITUD_CADENA','LLAMAR_SINTAXIS_CONCATENAR_CADENAS','LLAMAR_SINTAXIS_FUNCIONES',
                                   'LLAMAR_SINTAXIS_ES_PAR','LLAMAR_SINTAXIS_CADENA_MINUSCULA','LLAMAR_SINTAXIS_CADENA_MAYUSCULA',
                                   'LLAMAR_SINTAXIS_OBTENER_SUBCADENA']:
           self.definirFuncion()
        else:
           self.declararTipoDato()
        

#FIN DECLARACIONES DE VARIABLES
