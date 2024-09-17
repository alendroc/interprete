import re
#comando para instalar la libreria de analizador lexico pip install ply
#import ply.lex as lex

keywords = {
    'NUM': r'\bnum\b',               # Declaración de entero
    'DEC': r'\bdec\b',               # Declaración de float
    'SIM': r'\bsim\b',               # Declaración de char
    'BOOL': r'\bbool\b',             # Declaración de booleano
    'NULO': r'\bnulo\b',             # Declaración de valor nulo
    'CADENA': r'\bcadena\b',         # Declaración de string
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
    'CAR': r'\'\w\''
    }


class analisisLexico:
    def __init__(self):
        self.tokens = []

    def insert(self, token_type, token_value):
        self.tokens.append((token_type, token_value))


def tokenizar(tex):
    lexer=analisisLexico()
    
    tokenRegex='|'.join(f'(?P<{name}>{pattern})' for name, pattern in keywords.items())
    pos = 0
    pattern = re.compile(tokenRegex)
    while pos < len(tex):
        match = pattern.match(tex,pos)
        if match:
            token_type=match.lastgroup
            token_value = match.group()
            #print(f"{token_type}, {token_value})")
            lexer.insert(token_type,token_value)
            pos += len(token_value)  # Avanzar la posición en el texto
        else:
            #print(f"(Carácter no reconocido: {tex[pos]})")
            pos += 1  # Avanzar manualmente si no se reconoce el carácter
    for token in lexer.tokens:
        print(token)

prueba= """num numeros = 33:
cadena texto es = "texto":
"""
#print(splitFinal(prueba))
tokenizar(prueba)





    