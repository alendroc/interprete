class AnalisisSemantico:
    def __init__(self, variables):
        self.variables = variables

    def verificarTipoVar(self, tipo, valor):
        if tipo == "NUM":
            if isinstance(valor, bool):
                return False, f"Error semántico: Se esperaba un número, pero se encontró '{valor}'"
            if not isinstance(valor, (int, float)):
                return False, f"Error semántico: Se esperaba un número, pero se encontró '{valor}'"
        elif tipo == "SIM":
            if not isinstance(valor, str) or len(valor) != 1:
                return False, f"Error semántico: Se esperaba un solo carácter, pero se encontró '{valor}'"
        elif tipo == "CADENA":
            if not isinstance(valor, str):
                return False, f"Error semántico: Se esperaba una cadena, pero se encontró '{valor}'"
        elif tipo == "BOOL":
            if not isinstance(valor, bool):
                if valor == 1:
                   return True, None
                elif valor == 0:
                    return True, None
                return False, f"Error semántico: Se esperaba un valor booleano, pero se encontró '{valor}'"
        return True, None
    


    def verificarNumero(self, valor):
        if valor is None:
            return False, "Error semántico: Se encontró un valor nulo (None)"
        if not isinstance(valor, (int, float)):
            return False,f"Error semántico: Se esperaba un número, pero se encontró '{valor}'"
        return True,None



    def verificarDeclaracion(self, nombreVariable):
        if nombreVariable not in self.variables:
            return False, f"Error semántico: La variable '{nombreVariable}' no ha sido declarada."
        return True, None

    def verificarCompatibilidad(self, tipoVariable, valorAsignado):
        valido, error = self.verificarTipoVar(tipoVariable, valorAsignado)
       
        # print(f"VARIABLE: {tipoVariable}, VALOR: {valorAsignado}" )
        
        if not valido:
            return False, error
        return True, None

