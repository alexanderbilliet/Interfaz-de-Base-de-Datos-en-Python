import logging
import datetime
import val

def decorador_alta(funcion):
    """ decorador que observa el evento de alta en la base de datos"""
    def inner(*args, **kwargs):
        funcion(*args, **kwargs)
        print("esto es un decorador que avisa --> INGRESO NUEVO DE REGISTRO")
        logging.info("""ALTA DE REGISTRO
        Registro Agregado:
        - Nombre: %s
        - Descripcion: %s
        - Dia: %s
        - Hora: %s """,
        args[1],
        args[2],
        datetime.datetime.now().date(),
        datetime.datetime.now().time())
    return inner

def decorador_elimina(funcion):
    """ Decorador que observa al evento de baja de la base de datos"""
    def inner(*args, **kwargs):
        funcion(*args, **kwargs)
        print("esto es un decorador que avisa --> ELIMINACION DE REGISTRO")
        logging.info("""ELIMINACION DE REGISTRO
        Dato Eliminado:
        - id = %s
        - Dia: %s
        - Hora: %s """,
        args[1][0].get(),
        datetime.datetime.now().date(),
        datetime.datetime.now().time())

    return inner

def decorador_modifica(f):
    """ Decorador que observa al evento de modificación de la base de datos"""
    def inner(*args, **kwargs):
        if val.validar(args[1][1].get()):
            f(*args,**kwargs)
            print("esto es un decorador que avisa --> MODIFICACION DE REGISTRO")
            logging.info("""MODIFICACION DE REGISTRO
            Dato Modificado:
            - id = %s
            - Nuevo Titulo: %s
            - Nueva Descripcion: %s
            - Dia: %s
            - Hora: %s """,
            args[1][0].get(),
            args[1][1].get(),
            args[1][2].get(),
            datetime.datetime.now().date(),
            datetime.datetime.now().time())
        else:
            f(*args,**kwargs)
            print("""esto es un decorador que avisa -->
            INTENTO MODIFICACION DE REGISTRO NO VALIDADO""")
            logging.info("""INTENTO MODIFICACION DE REGISTRO NO VALIDADO
            Dato que se intentó modificar :
            - id = %s
            - Nuevo Titulo: %s
            - Nueva Descripcion: %s
            - Dia: %s
            - Hora: %s """,
            args[1][0].get(),
            args[1][1].get(),
            args[1][2].get(),
            datetime.datetime.now().date(),
            datetime.datetime.now().time())
    return inner