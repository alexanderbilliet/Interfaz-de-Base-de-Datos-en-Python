"""
ENTREGA FINAL: DIPLOMATURA EN PYTHON - UTN [2021]
"""

import datetime
import logging
from tkinter import Tk
from vista import VistaApp

class MiApp:
    """
    Clase que incializa una instancia de la clase VistaApp.

    ...
    Atributos:
    ----------
    window : Tk()
        Top level widget sobre el cual se abrirá la vista de la aplicación.
    """

    def __init__(self, window):
        self.ventana = window
        VistaApp(self.ventana)

if __name__ == '__main__':
    logging.basicConfig(filename='App.log', level=logging.INFO)
    logging.info('App iniciada. Dia: %s con Horario: %s',
                datetime.datetime.now().date(), datetime.datetime.now().time())
    root = Tk()
    obj = MiApp(root)
    root.mainloop()
    logging.info('App cerrada. Dia: %s con Horario: %s',
                datetime.datetime.now().date(), datetime.datetime.now().time())