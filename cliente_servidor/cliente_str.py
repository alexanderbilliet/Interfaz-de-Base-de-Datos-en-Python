import socket
import sys

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Mensaje que manda cliente a servidor:
mensaje = "Hola. Soy un cliente que manda un string!"
# Envio de mensaje:
sock.sendto(mensaje.encode("UTF-8"), (HOST, PORT))
# Recepcion de respuesta de parte del servidor:
received = sock.recvfrom(1024)
# Impresion de mensajes enviados y recibidos:
print("Mensaje enviado a servidor: ")
print(mensaje)
print("Mensaje recibido desde el servidor: ")
print(received[0].decode("UTF-8"))
#print(received)
