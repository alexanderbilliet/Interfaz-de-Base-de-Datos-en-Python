# ENTREGA FINAL: Interfaz de Base de Datos en Python

Este es el proyecto final del curso “Diplomatura en Python” del Centro de E-Learning de la Universidad Tecnológica Nacional.


La aplicación consiste en una interfaz gráfica hecha a través de Tkinter que permite interactuar con una base de datos SQLite (alta, baja, modificación y consulta de registros).

Además, cuenta con observadores de eventos, implementados a través de decoradores, que almacenan la información sobre los eventos realizados en un registro de log.

Por último, se le agregó también la posibilidad de prender un servidor y que interactúe con dos clientes, uno que envía información en hexadecimal y otro en string. Además, la aplicación está estructurada con patrón MVC y con POO y la interacción con SQLite se hace a través de un ORM.

## La aplicación consta de 8 módulos en total, organizados de la siguiente manera:

1.	[controlador.py](#controlador.py)
2.	[vista.py](#vista.py)
3.	[modelo.py](#modelo.py)
4.	[decoradores.py](#decoradores.py)
5.	[val.py](#val.py)
6.	[cliente_servidor](#cliente_servidor)
    - [udp_server_t.py](#udp_server_t.py)
    - [cliente_hex.py](#cliente_hex.py)
    - [cliente_str.py](#cliente_str.py)

## controlador.py
<a name="#controlador.py"></a>

Desde donde se lanza la aplicación.

En este módulo se encuentra la clase **MiApp** que inicializa una instancia de la clase **VistaApp**.
Cada vez que se corre este módulo se graba en el registro de log el inicio y finalización de la aplicación, así como el horario cuando estas acciones fueron ejecutadas.

## vista.py
<a name="#vista.py"></a>

Es el módulo donde está estructurada la interfaz gráfica de la aplicación.

La clase **VistaApp** posee un método constructor que diseña la ventana principal, los campos de entrada, el treeview, y los botones.
Por fuera del constructor están los métodos que se encargan de llamar a los métodos del módulo ***modelo.py***: Aquí se encuentran tanto los métodos para llamar a la clase **Servidor** como a la clase **BaseDeDatos** que permiten prender y apagar el servidor e interactuar con la base de datos.

## modelo.py
<a name="#modelo.py"></a>
Es el módulo donde están las clases que permiten a la aplicación interactuar con la base de datos y generar la conexión cliente – servidor.

Tanto la clase **BaseModel** como **Noticia** generan la base de datos utilizando el ORM peewee.

Dentro de la clase **BaseDeDatos** se estructuran todos los métodos necesarios para hacer un alta, baja, consulta y modificación de registros de la base de datos SQLite. Cada método tiene asignado su respectivo decorador para registrar el evento en el registro de log.

Dentro de la clase **Servidor** están los tres métodos que lanzan, activan y detienen al servidor.

## decoradores.py
<a name="#decoradores.py"></a>

En este módulo se definen funcionalmente tres decoradores para las acciones de “alta”, “baja” y “modificación” de base de datos.

Cada decorador, avisa sobre el tipo de evento (alta, baja o modificación), el día y la hora cuando fueron realizados y algún dato adicional sobre el registro afectado (nombre y descripción en caso de un alta, id en caso de una eliminación y ID y nuevo nombre y descripción en caso de una modificación).

## val.py
<a name="#val.py"></a>

Este módulo contiene a la función validar(cad) que retorna un booleano True si la cadena que se pasa respeta al patrón definido al interior de la función y False si no lo hace.

En la práctica la aplicación valida el campo “título” para evitar que se ingresen caracteres no alfabéticos. Esta validación se hace tanto en el momento de dar de alta un registro como en el momento de modificación.

## udp_server_t.py
<a name="#udp_server_t.py"></a>

Módulo que contiene al funcionamiento del servidor. Está estructurado con la clase **MyUDPHandler(socketserver.BaseRequestHandler)** que contiene al método Handle que hace el request al cliente.
Luego un try que intenta hacer el decode de la información recibida desde el cliente.
En caso de que este decode falle, se levanta una excepción que hace el decode en caso de que lo recebido esté en formato hexadecimal.
Para ambos casos luego el servidor envía una respuesta al cliente.

## cliente_hex.py
<a name="#cliente_hex.py"></a>

Modulo que implementa un cliente que se conecta con el servidor de la aplicación. Envía un mensaje en hexadecimal y recibe una respuesta del servidor.

## cliente_str.py
<a name="#cliente_str.py"></a>

Modulo que implementa un cliente que se conecta con el servidor de la aplicación. Envía un mensaje en formato string y recibe una respuesta del servidor.