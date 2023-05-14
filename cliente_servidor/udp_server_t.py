import socketserver
import binascii
#global HOST
global PORT

class MyUDPHandler(socketserver.BaseRequestHandler):


    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        # El try intenta hacer decode de la data. Si llegara a ser Hex, levanta
        # directamente el Except:
        try:
            # Guardo la data en una variable para que si falla el decode me
            # mande enseguida al except:
            data_decoded = data.decode("UTF-8")
            # Luego, imprime la info recibida desde el cliente:
            print("Mensaje recibido desde cliente: ")
            print(data_decoded)
            # Luego, prepara una rta para enviar a cliente:
            respuesta_str = "Hola. Soy el servidor contestando a un cliente \
que mando un string"
            # Se empaqueta la rta:
            respuesta_empacada = respuesta_str.encode("UTF-8")
            # Y se manda al cliente:
            socket.sendto(respuesta_empacada, self.client_address)
            # Imprime info enviada a cliente:
            print("Mensaje enviado al cliente: ")
            print(respuesta_str)

        # Si falló "data.decode" arriba, se dispara este except:
        except:

            # Convierte la info recibida en bytearray:
            binary_field = bytearray(data)
            # Luego hace el decode:
            dato_recibido2 = binascii.hexlify(binary_field).decode("utf-8")
            # Luego, se prepara la rta al cliente:
            value2 = 0xA0
            packed_data_2 = bytearray()
            packed_data_2 += value2.to_bytes(1, "big")
            # Y se envia la rta al cliente:
            socket.sendto(packed_data_2, self.client_address)

            # Finalmente, se imprimen los mensajes recibidos y enviados:
            print("Mensaje recibido desde cliente: ")
            print(dato_recibido2)
            print("Mensaje enviado al cliente: ")
            print(binascii.hexlify(packed_data_2).decode("utf-8"))

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    with socketserver.UDPServer((HOST, PORT), MyUDPHandler) as server:
        server.serve_forever()