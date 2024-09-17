import re

keywords = {
    'NUM': r'\bnum\b',               # Declaración de entero
    'DEC': r'\bdec\b',               # Declaración de float
    'SIM': r'\bsim\b',               # Declaración de char
    'BOOL': r'\bbool\b',             # Declaración de booleano
    'NULO': r'\bnulo\b',             # Declaración de valor nulo
    'CADENA': r'\bcadena\b',         # Declaración de string
    'Y':r'\b\&{2}\b|\&{2}',               #Operador and
    'O':r'\b\|{2}\b|\|{2}',               #Operador or
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
    'IGUALDAD': r'\bes\b',          # Comparación de igualdad
    'NEGACION': r'\bno\b',          # Negación (No igual a)
    'FIN_LINEA': r':',          # Fin de línea
    'ID': r'[a-zA-Z_][a-zA-Z0-9_]*',  # Identificadores
    'NUMERO': r'\d+(\.\d+)?',   # Números (enteros o decimales)
    'TEXTO': r'"[^"]*"',        # Strings entre comillas
    'CAR': r'\'\w\'',
    'ESPACIOS': r'\s'
    }


class analisisLexico:
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
                if token_type != 'ESPACIOS':
                    self.insert(token_type, token_value)    
                pos += len(token_value)  
            else:
                print(f"(Carácter no reconocido: {tex[pos]})")
                pos += 1 
        for token in self.tokens:
            print(token)

prueba= """num numeros = 90:
cadena texto es = "texto":
"""
#print(splitFinal(prueba))

analisisLexico().tokenizar(prueba)





    