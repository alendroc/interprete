from lexico import analisisLexico as lex

class analisisSintactico:
    def __init__(self,tokens):
        self.tokens = tokens
        self.pos=0
        self.tokenActual= tokens[0] if tokens else None
        self.variables = {}
        self.linea=1
        
    def consumirToken(self, token):
        if self.tokenActual and self.tokenActual[0] == token:
            self.pos += 1
            #print(self.tokenActual)
            if self.pos < len(self.tokens):
                self.tokenActual = self.tokens[self.pos]

            else:
                self.tokenActual = None
        else:
            print(f"Error sintáctico: Se esperaba {token}, pero se encontró {self.tokenActual}")
           


#DECLARACIONES DE VARIABLES
    def declararTipoDato(self):
        if self.tokenActual[0] in ['NUM', 'SIM', 'CADENA', 'BOOL']:
            self.declaraciones()
        else:
            print(f"Error sintáctico: Declaración inesperada en {self.tokenActual}")
            self.tokenActual = None


    def declaraciones(self):
        tipo = self.tokenActual[0]
        self.consumirToken(tipo)
        nombreVariable = self.tokenActual[1]
        if nombreVariable in self.variables:
            print(f"variable {nombreVariable} ya antes declarada")
            self.tokenActual = None
            return
        self.consumirToken('ID')
        self.consumirToken('ASIGNAR')

#NO SÉ SI VA EN SEMANTICO

        if tipo =="NUM":
            valorExpresion = self.expresionesAritm()
            if not isinstance(valorExpresion,(int, float)):
                print(f"Error: Asignación de valor incompatible a una variable de tipo NUM en '{nombreVariable}'")
                return
            
        elif tipo == "SIM":
            valorExpresion = self.analizarVariables()
            if not isinstance(valorExpresion, str) or len(valorExpresion) != 1:
                print(f"Error: Asignación de valor incompatible a una variable de tipo SIM en '{nombreVariable}'")
                return
            
        elif tipo == "CADENA":
            valorExpresion = self.analizarVariables()
            if not isinstance(valorExpresion, str):
                print(f"Error: Asignación de valor incompatible a una variable de tipo CADENA en '{nombreVariable}'")
                return
            
        elif tipo == "BOOL":
            valorExpresion = self.analizarVariables()
            if not isinstance(valorExpresion, bool):
                if valorExpresion == 1:
                    valorExpresion = True
                elif valorExpresion == 0:
                    valorExpresion = False
                else:
                    print(f"Error: Asignación de valor incompatible a una variable de tipo BOOL en '{nombreVariable}'")
                    return
#TERMINA

        self.consumirToken('FIN_LINEA')
        self.variables[nombreVariable] = valorExpresion
        print(f"Declaración de {tipo} {nombreVariable} = {valorExpresion}")

#EXPRESIONES ARITMETICAS PARA ASIGNAR NUMEROS
    def expresionesAritm(self):
        result = self.multiplicacionDivision()
        while self.tokenActual and self.tokenActual[0] in ['SUMA', 'RESTA']:
            token = self.tokenActual
            if token[0] == 'SUMA':
                self.consumirToken('SUMA')
                result += self.multiplicacionDivision()
            elif token[0] == 'RESTA':
                self.consumirToken('RESTA')
                result -= self.multiplicacionDivision()
        return result

    def multiplicacionDivision(self):
        result = self.asignarParentesis()
        while self.tokenActual and self.tokenActual[0] in ['MULT', 'DIV']:
            token = self.tokenActual
            if token[0] == 'MULT':
                self.consumirToken('MULT')
                result *= self.asignarParentesis()
            elif token[0] == 'DIV':
                self.consumirToken('DIV')
                result /= self.asignarParentesis()
        return result
    

    def asignarParentesis(self):
            if self.tokenActual[0] == 'PARENTESIS_I':
                self.consumirToken('PARENTESIS_I')
                result = self.expresionesAritm()
                self.consumirToken('PARENTESIS_D')
                return result
            return self.analizarVariables()
    
#FIN DE ASIGNACION DE NUMEROS

    def analizarVariables(self):
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
            return nombreVariable
        else:
            print('Token inesperado al asignar valor')
            return None
        
#FIN DECLARACIONES DE VARIABLES

prueba= """num n = (90 + 20 -10) / 2*2:
bool n2 = falso:
sim n3 = '@':
"""


le=lex()
le.tokenizar(prueba)
aS=analisisSintactico(le.tokens)

while aS.tokenActual:
    aS.declararTipoDato()
    if not aS.tokenActual:  # Si no hay más tokens, salir del bucle
        break

#HAY COSAS QUE HAY QUE PASARLAS AL ANALISIS SEMANTICO COMO LAS VALIDACIONES DE TIPOS Y VERIFICAR DECLARACIONES
