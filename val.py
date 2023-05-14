import re
def validar(cad):
    """
    Funcion que retorna un booleano.
    True si la cadena cumple con el patrón.
    False si la cadena no cumple con el patrón.

    """
    patron="^[A-Za-z]+(?:[ _-][A-Za-z]+)*$"
    try:
        re.match(patron,cad)
        if(re.match(patron,cad)):
            return True
        else:
            return False
    except:
        return False
