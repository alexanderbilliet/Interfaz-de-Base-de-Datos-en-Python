from tkinter import *
from tkinter.messagebox import *
from peewee import OperationalError
import modelo
from tkinter import ttk
import val
import logging

class VistaApp:
    """
    Clase que genera la vista que tendrá el usuario de la aplicación.

    ...

    Métodos:
    ----------
    crear_base_datos_c_peewee()
        Metodo que crea la base de datos en Sql
    pasar_objeto_eliminar()
        Metodo que llama al método "eliminar" de la clase BaseDeDatos()
    pasar_objeto_modificar
        Metodo que llama al método "modificar()" de la clase BaseDeDatos()
    mostrar()
        Metodo que llama al método "f_mostrar()" de la clase BaseDeDatos()
        y ademas resetea el Treeview.
    alta()
        Funcion que llama al método "f_alta()" de la clase BaseDeDatos()
    para_f_borrar(p1)
    """

    def __init__(self, window):
        """
        Parámetros:
        ----------
        window : Tk()
            Top level widget sobre el cual se abrirá la vista de la aplicación.
        """

        ################################
        ################################
        # Ventana principal
        ################################
        ################################
        self.root = window
        self.root.title("App")

        titulo = Label(self.root, text="ATENCION: Si no esta creada la bbdd, \
antes de tocar cualquier boton debe PRIMERO tocar el boton 'Crear bd'"
        , bg="DarkOrchid3",
        fg="thistle1",
        height=1,
        width=60)
        titulo.grid(row=0, column=0, columnspan=4, padx=1, pady=1, sticky=W+E)

        Label(self.root, text="Título").grid(row=1, column=0, sticky=W)
        Label(self.root, text="Descripción").grid(row=2, column=0, sticky=W)

        ################################
        ################################
        # de campos de entrada
        ################################
        ################################
        self.a_val, self.b_val = StringVar(), StringVar()
        w_ancho = 20
        self.entrada_titulo = Entry(self.root, textvariable = self.a_val,
                                                               width = w_ancho)
        self.entrada_titulo.grid(row = 1, column = 1)
        self.entrada_descripcion = Entry(self.root, textvariable = self.b_val,
                                                               width = w_ancho)
        self.entrada_descripcion.grid(row = 2, column = 1)

        ################################
        ################################
        # Treeview
        ################################
        ################################
        self.tree = ttk.Treeview(height = 10, columns = 3)
        self.tree["columns"]=("one","two")
        self.tree.grid(row = 7, column = 0, columnspan = 3)
        self.tree.heading("#0",text="ID",anchor=CENTER)
        self.tree.heading("one", text = 'Título', anchor = CENTER)
        self.tree.heading("two", text = 'Descripción', anchor = CENTER)

        ################################
        ################################
        # Botones
        ################################
        ################################
        ttk.Button(self.root, text = 'Mostrar registros existentes',
               command = lambda:self.mostrar()).grid( row = 5, columnspan = 3,
                                                               sticky = W + E)

        Button(self.root, text="Crear bd",
        command=lambda:self.crear_base_datos_c_peewee()).grid(row=6, column=0)
        Button(self.root, text="Alta", command=lambda:self.alta()).grid(row=6,
                                                                     column=1)
        Button(self.root, text='Eliminar',
              command=lambda:self.pasar_objeto_eliminar()).grid(row=11, column=1)
        Button(self.root, text='Modificar',
             command=lambda:self.pasar_objeto_modificar()).grid(row=11, column=2)

        self.boton_prender_servidor = Button(self.root, text="Prender Servidor",
         command= lambda:self.pasar_prender_servidor())
        self.boton_prender_servidor.grid(row=1, column=2)

        Button(self.root, text="Apagar Servidor",
         command= lambda:self.pasar_apagar_servidor()).grid(row=2, column=2)

    ################################
    ################################
    # Métodos llamadores
    ################################
    ################################

    #VARIABLES GLOBALES
    theproc = ""

    def pasar_prender_servidor(self,):
        print("prendiendo el servidor...")
        objeto_prender_servidor = modelo.Servidor()
        objeto_prender_servidor.activar_servidor()
        self.orig_color = self.boton_prender_servidor.cget("background")
        self.boton_prender_servidor.configure(bg="red")

    def pasar_apagar_servidor(self,):
        print("apagando el servidor...")
        objeto_apagar_servidor = modelo.Servidor()
        objeto_apagar_servidor.stop_server()
        self.boton_prender_servidor.configure(bg=self.orig_color)

    def crear_base_datos_c_peewee(self,):
        """Crea la base de datos y tabla en SQL."""
        try:
            modelo.db.connect()
            modelo.db.create_tables([modelo.Noticia])
            showinfo("APP", "Se ha creado la base de datos")
        except OperationalError:
            showinfo('-', 'Debe crear BD antes que tocar cualquier otro boton.\
Cierre la aplicación y vuelva a iniciarla y toque el boton de crear BD')

    def pasar_objeto_eliminar(self,):
        """ Llama al método eliminar() de la clase BaseDeDatos() """
        objeto_eliminar = modelo.BaseDeDatos()
        objeto_eliminar.eliminar(self)

    def pasar_objeto_modificar(self,):
        """ Llama al método modificar() de la clase BaseDeDatos() """
        objeto_modificar = modelo.BaseDeDatos()
        objeto_modificar.modificar(self)

    def mostrar(self,):
        """ Actualiza Treeview y llama al método f_mostrar() de la clase
        BaseDeDatos() """
        # limpieza de tabla
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # llamada al método mostrar de la clase BaseDeDatos:
        objeto_mostrar = modelo.BaseDeDatos()
        resultado = objeto_mostrar.f_mostrar()
        # Insertar registros en el Treeview:
        for fila in resultado:
            self.tree.insert('', 0, text = fila[0], values = (fila[1],fila[2]))

    def alta(self,):
        """Llama al método f_alta de la clase BaseDeDatos()"""
        cadena=self.a_val.get() #obtenemos la cadena del campo de texto
        if(val.validar(cadena)):
            objeto_alta = modelo.BaseDeDatos()
            objeto_alta.f_alta(self.a_val.get(), self.b_val.get())
        else:
            logging.info('ALTA DE DATOS FALLIDA: la cadena " %s " no cumplio \
con la validacion', cadena)
            showinfo('No Validado',
            'El campo de título no cumple los requisitos, ingrese datos alfabe\
ticos')
        self.mostrar()

