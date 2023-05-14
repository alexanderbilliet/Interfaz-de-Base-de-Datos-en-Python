from enum import unique
import threading
import time
from tkinter import *
from tkinter.messagebox import showerror, showinfo
from peewee import *
from decoradores import decorador_alta, decorador_elimina, decorador_modifica
import os
from pathlib import Path
import subprocess
import sys
import val

#VARIABLES GLOBALES
theproc = ""

# Implementación de la base de datos en Peewee:

db = SqliteDatabase('app_nivel_avanzado.db')

class BaseModel(Model):
    class Meta:
        database = db

class Noticia(BaseModel):
    titulo = CharField(unique=True)
    descripcion = TextField()

class BaseDeDatos:
    """
    Clase que contiene métodos para interactuar con la base de datos de SQL

    ...

    Métodos:
    ----------
    f_alta(self, titulo, descripcion))
        Da de alta registro en base SQL
        titulo -> parámetro String que irá a la base de datos.
        descripcion -> parámetro String que irá a la base de datos.

    crear_form_eliminar(self, root, campos)
        Genera una ventana intermedia de la app para elegir qué registro elimi-
        nar de la base datos.
        root -> Toplevel widget de tkinter
        campos -> Columnas de la tabla de SQL.

    show(self, vars, popup_guardar)
        Elimina la ventana intermedia.

    elimina(self, variables, popup_eliminar, elobjeto)
        Elimina el registro según el ID seleccionado
        variables -> Objeto Entry de Tkinter
        popup_eliminar -> Toplevel() widget de Tkinter
        elobjeto ->

    eliminar(self, objeto)
        Metodo intermedio que llama a crear_form_eliminar y genera dos botones

    modifica(self, variables, popup_modificar, elobjeto)
        Metodo que actualiza el registro en la base de SQL.

    modificar(self, objeto)
        Metodo intermedio que llama a crear_form_eliminar y genera dos botones

    crear_form_modificar(self, root, campos)
        Genera una ventana intermedia de la app para elegir qué registro elimi-
        nar de la base datos.

    f_mostrar(self, )
        Devuelve en 'resultado' una seleccion de la base de datos ordenada por
        ID.

    """
    def __init__(self,):
        pass

    ###################################################################
    # ALTA ############################################################
    ###################################################################

    @decorador_alta
    def f_alta(self, titulo, descripcion):
        """
        Método que da de alta un registro en la base de datos

        Parámetros:
        titulo -> un string con el título que se quiere guardar en la bbdd
        descripcion -> string con descr que se quiere guardar en la bbdd

        """
        noticia = Noticia()
        noticia.titulo = titulo
        noticia.descripcion = descripcion
        try:
            noticia.save()
        except IntegrityError:
            showerror("Error de Integridad",
            "El Titulo ingresado ya se encuentra en la base de datos")

    ###################################################################
    # ELIMINAR ########################################################
    ###################################################################

    def crear_form_eliminar(self, root, campos):
        """
        Genera una ventana intermedia de la app para elegir qué registro elimi-
        nar de la base datos.
        Parámetros:
        root -> Toplevel widget de tkinter
        campos -> Columnas de la tabla de SQL.

        """
        formulario = Frame(root)
        div1 = Frame(formulario, width=100)
        div2 = Frame(formulario, padx=7, pady=2)
        formulario.pack(fill=X)
        div1.pack(side=LEFT)
        div2.pack(side=RIGHT, expand=YES, fill=X)
        variables = []
        lab = Label(div1, width=10, text="ID")
        ent = Entry(div2, width=30, relief=SUNKEN)
        lab.pack(side=TOP)
        ent.pack(side=TOP, fill=X)
        var = StringVar()
        ent.config(textvariable=var)
        var.set('---')
        variables.append(var)
        return variables

    def show(self, vars, popup_guardar):
        """ Elimina la ventana intermedia en tkinter"""
        popup_guardar.destroy()

    @decorador_elimina
    def elimina(self, variables, popup_eliminar, elobjeto):
        """
        Elimina el registro según el ID seleccionado
        Parámetros:
        variables -> Objeto Entry de Tkinter
        popup_eliminar -> Toplevel() widget de Tkinter

        """
        popup_eliminar.destroy()
        lista = []
        for variable in variables:
            lista.append(variable.get())
        borrar = Noticia.get(Noticia.id == lista[0])
        borrar.delete_instance()
        elobjeto.mostrar()

    def eliminar(self, objeto):
        """
        Metodo intermedio que llama a crear_form_eliminar y genera dos
        botones
        """
        popup_eliminar = Toplevel()
        vars_eliminar = self.crear_form_eliminar(popup_eliminar, "ID")
        Button(popup_eliminar, text='OK', command=(lambda:
                               self.show(vars_eliminar, popup_eliminar))).pack()
        Button(popup_eliminar, text='eliminar', command=(lambda:
                    self.elimina(vars_eliminar, popup_eliminar, objeto))).pack()

        popup_eliminar.grab_set()
        popup_eliminar.focus_set()
        popup_eliminar.wait_window()

    ###################################################################
    # MODIFICAR #######################################################
    ###################################################################

    @decorador_modifica
    def modifica(self, variables, popup_modificar, elobjeto):
        """
        Metodo que actualiza el registro en la base de SQL

        """
        # Actualizado con Peewee:
        popup_modificar.destroy()
        if val.validar(variables[1].get()):
            lista = []
            for variable in variables:
                lista.append(variable.get())
            actualizar = Noticia.update(titulo = lista[1],
                        descripcion = lista[2]).where(Noticia.id == lista[0])
            try:
                actualizar.execute()
                elobjeto.mostrar()
            except IntegrityError:
                showerror("Error de Integridad",
                "El Titulo ingresado ya se encuentra en la base de datos")
                elobjeto.mostrar()
        else:
            showinfo('No validado','El campo de título no cumple los requisito\
s, ingrese datos alfabeticos' )

    def modificar(self, objeto):
        """
        Metodo intermedio que llama a crear_form_modificar y genera los
        botones para registrar la modificacion.

        """

        popup_modificar = Toplevel()
        vars_modificar = self.crear_form_modificar(popup_modificar,
                                                ('id', 'Titulo','Descripcion'))
        Button(popup_modificar, text='OK', command=(lambda:
                             self.show(vars_modificar, popup_modificar))).pack()
        Button(popup_modificar, text='modificar', command=(lambda:
                 self.modifica(vars_modificar, popup_modificar, objeto))).pack()

        popup_modificar.grab_set()
        popup_modificar.focus_set()
        popup_modificar.wait_window()

    def crear_form_modificar(self, root, campos):
        """
        Genera una ventana intermedia de la app para elegir qué registro elimi-
        nar de la base datos.

        """

        formulario = Frame(root)
        div1 = Frame(formulario, width=100)
        div2 = Frame(formulario, padx=7, pady=2)
        formulario.pack(fill=X)
        div1.pack(side=LEFT)
        div2.pack(side=RIGHT, expand=YES, fill=X)
        variables = []
        for field in campos:
            lab = Label(div1, width=10, text=field)
            ent = Entry(div2, width=30, relief=SUNKEN)
            lab.pack(side=TOP)
            ent.pack(side=TOP, fill=X)
            var = StringVar()
            ent.config(textvariable=var)
            var.set('---')
            variables.append(var)
        return variables

    ###################################################################
    # MOSTRAR #########################################################
    ###################################################################

    def f_mostrar(self, ):
        """
        Devuelve en 'resultado' una seleccion de la base de datos ordenada por
        ID.

        """
        resultado = db.execute_sql('SELECT * FROM noticia ORDER BY id ASC')
        return resultado

class Servidor():
    """
    Clase que contiene métodos para prender y apagar el servidor

    ...

    Métodos:
    ----------
    lanzar_servidor(self, var)
        Se le pasa una var True y prende la conexión del servidor.

    stop_server(self, )
        Detiene al servidor.

    activar_servidor(self,)
        llama a lanzar_servidor con un thread específico.

    """
    def __init__(self,):
        pass
        self.raiz = Path(__file__).resolve().parent
        self.ruta_server = os.path.join(self.raiz, 'cliente_servidor',
                                                     'udp_server_t.py')

    def lanzar_servidor(self, var):
        print("Servidor Lanzado")
        the_path =  self.ruta_server
        if var==True:
            global theproc
            theproc = subprocess.Popen([sys.executable, the_path])
            theproc.communicate()
        else:
            print("Else del activar servidor")

    def stop_server(self, ):
        global theproc
        if theproc !="":
            theproc.kill()
            print("servidor detenido")
            showinfo("App", "Servidor Desactivado")

    def activar_servidor(self,):
        if theproc != "":
            theproc.kill()
            threading.Thread(target=self.lanzar_servidor, args=(
                True,), daemon=True).start()
            time.sleep(1)
            showinfo("App", "Servidor Activado")
        else:
            threading.Thread(target=self.lanzar_servidor, args=(
                True,), daemon=True).start()
            time.sleep(1)
            showinfo("App", "Servidor Activado")


