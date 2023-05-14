import socket
import sys
import binascii

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Mensaje que manda cliente a servidor:
mi_valor = 0x00003EF5
# Empaque del valor a enviar a cliente:
packed_data = bytearray()
packed_data += mi_valor.to_bytes(4, "big")
mensaje = packed_data
# envia mensaje a servidor:
sock.sendto(mensaje, (HOST, PORT))
# Recibe rta desde el servidor:
received = sock.recvfrom(1024)

# Impresion de mensajes enviados y recibidos:
print("mensaje enviado a servidor: ")
print(binascii.hexlify(mensaje).decode("utf-8"))
print("mensaje recibido desde servidor: ")
print(binascii.hexlify(received[0]).decode("utf-8"))
