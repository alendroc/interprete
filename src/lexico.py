import re

keywords = {
    'NUM': r'\bnum\b',               # Declaración de numerico
    'SIM': r'\bsim\b',               # Declaración de char
    'BOOL': r'\bbool\b',             # Declaración de booleano
    #'NULO': r'\bnulo\b',             # Declaración de valor nulo
    'CADENA': r'\bcadena\b',         # Declaración de string
    'Y':r'\b\&{2}\b|\&{2}',          #Operador and
    'O':r'\b\|{2}\b|\|{2}',          #Operador or
    'SUMA': r'\+',               # Operador suma
    'RESTA': r'\-',              # Operador resta
    'MULT': r'\*',               # Operador multiplicación
    'DIV': r'/',                 # Operador división
    'MENOR': r'<',               # Operador menor que
    'MENOR_IGUAL': r'<=',        # Operador menor o igual que
    'MAYOR': r'>',               # Operador mayor que
    'MAYOR_IGUAL': r'>=',        # Operador mayor o igual que
    'ASIGNAR': r'=',             # Asignación de valor
    'DIFERENTE': r'<>',          # Diferente
    'PARENTESIS_I': r'\(',       # Parentesis izquierdo
    'PARENTESIS_D': r'\)',       # Parentesis derecho
    'CORCHETE_I': r'\[',         # Corchete izquierdo
    'CORCHETE_D': r'\]',         # Corchete derecho
    'LLAVE_I': r'\{',            # Llave izquierdo
    'LLAVE_D': r'\}',            # Llave derecha
    'IGUALDAD': r'\bes\b',       # Comparación de igualdad
    'NEGACION': r'\bno\b',       # Negación (No igual a)
    'FIN_LINEA': r':',           # Fin de línea
    'NUMERO': r'\d+(\.\d+)?',   # Números (enteros o decimales)
    'VERDADERO': r'\bverdadero\b|\b1\b',
    'FALSO': r'\bfalso\b|\b0\b',
    'TEXTO': r'"[^"]*"',        # Strings entre comillas
    'CAR': r"'(.)'",              # Caracter
    'SI': r'\bsi\b',            # si simula el if
    'SINO': r'\bsino\b',          # sino simula el else
    'ESPACIOS': r'\s',
    'SALTO_LINEA': r'\n',           #salto de linea
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',  # Identificadores
    'SEPARADOR': r'[,]',

    'LLAMAR_NUM_ALEATORIO': r'\$ALEATORIO',
    'LLAMAR_IMPRIMIR': r'\$IMPRIMIR', 
    'LLAMAR_OBTENER_FECHA_ACTUAL': r'\$OBTENER_FECHA',
    'LLAMAR_CONTAR_VOCALES': r'\$CONT_VOCALES',  
    'LLAMAR_POTENCIA': r'\$POTENCIA',
    'LLAMAR_LONGITUD_CADENA': r'\$LONGITUD', 
    'LLAMAR_SINTAXIS_DECLARACIONES': r'\$DECLARACIONES',
    'LLAMAR_SINTAXIS_FUNCIONES': r'\$FUNCIONES',
    'LLAMAR_SINTAXIS_CONCATENAR_CADENAS': r'\$CONCATENAR',

    'LLAMAR_SINTAXIS_ES_PAR': r'\$PAR',
    'LLAMAR_SINTAXIS_CADENA_MINUSCULA': r'\$MINUS',
    'LLAMAR_SINTAXIS_CADENA_MAYUSCULA': r'\$MAYUS',
    'LLAMAR_SINTAXIS_OBTENER_SUBCADENA': r'\$SUBCADENA'

    }


class AnalisisLexico:
    def __init__(self):
        self.tokens = []

    def insert(self, token_type, token_value):
        self.tokens.append((token_type, token_value))
        
        
    def tokenizar(self,tex):
        tokenRegex='|'.join(f'(?P<{name}>{pattern})' for name, pattern in keywords.items())
        pos = 0
        pattern = re.compile(tokenRegex)
        while pos < len(tex):
            match = pattern.match(tex,pos)
            if match:
                token_type=match.lastgroup
                token_value = match.group()

                if token_type == 'CAR' and len(token_value) != 3:
                     print(f"Error léxico: El carácter '{token_value}' no es válido. Se esperaba un solo carácter.")
                     pos += len(token_value)
                     continue

                if token_type != 'ESPACIOS':
                    self.insert(token_type, token_value)    
                pos += len(token_value)  
            else:
                #print(f"Error léxico: Carácter no reconocido: {tex[pos]}")
                pos += 1 
       





    