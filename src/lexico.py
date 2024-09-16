import re

class lexico:
    def __init__(self, cod_user):
        self.cod_user = cod_user
        self.tokens = []


def tokens(self):
        token_specification = [
            ('NUM', r'num'),               # Declaración de entero
            ('DEC', r'dec'),               # Declaración de float
            ('SIM', r'sim'),               # Declaración de char
            ('BOOL', r'bool'),             # Declaración de booleano
            ('NULO', r'nulo'),             # Declaración de valor nulo
            ('CADENA', r'cadena'),         # Declaración de string
            ('PLUS', r'\+'),               # Operador suma
            ('MINUS', r'-'),               # Operador resta
            ('MULT', r'\*'),               # Operador multiplicación
            ('DIV', r'/'),                 # Operador división
            ('MENOR', r'<'),                # Operador menor que
            ('MENOR_IGUAL', r'<='),          # Operador menor o igual que
            ('MAYOR', r'>'),             # Operador mayor que
            ('MAYOR_IGUAL', r'>='),       # Operador mayor o igual que
            ('ASIGNAR', r'='),              # Asignación de valor
            ('DIFERENTE', r'<>'),           # Diferente
            ('IGUALDAD', r'es'),            # Comparación de igualdad
            ('NEGACION', r'no'),                # Negación (No igual a)
            ('FIN_LINEA', r':'),             # Fin de línea
            ('ID', r'[a-zA-Z_][a-zA-Z0-9_]*'),  # Identificadores
            ('NUMERO', r'\d+(\.\d+)?'),    # Números (enteros o decimales)
            ('TEXTO', r'"[^"]*"')        # Strings entre comillas
        ]

prueba= "num numeros = 33"

    