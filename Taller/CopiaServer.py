import socket
import pickle
import time

class CopiaServer:
    def __init__(self, server_port, iva_port, suma_port):
        self.server_port = server_port
        self.iva_port = iva_port
        self.suma_port = suma_port

    def main(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(("localhost", self.server_port))
            server_socket.listen()

            print(f"Esperando conexiones en el puerto {self.server_port}")

            while True:
                client_socket, client_address = server_socket.accept()
                print(f"Conexión aceptada desde {client_address}")

                try:
                    self.handle_client(client_socket)
                except Exception as e:
                    print(f"Error al manejar la conexión del cliente: {e}")
                finally:
                    client_socket.close()

    def handle_client(self, client_socket):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as iva_socket:
                iva_socket.connect(("localhost", self.iva_port))

                productos = pickle.loads(client_socket.recv(1024))

                productos_con_iva = []
                for producto in productos:
                    try:
                        iva_socket.sendall(pickle.dumps(producto))
                        producto_con_iva = pickle.loads(iva_socket.recv(1024))
                        productos_con_iva.append(producto_con_iva)
                    except Exception as e:
                        print(f"No se pudo conectar a IvaNode. Aplicando IVA localmente: {e}")
                        productos_con_iva = self.apply_local_iva(productos)

                suma_precios = sum(producto['precio'] for producto in productos_con_iva)

                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as suma_socket:
                    suma_socket.connect(("localhost", self.suma_port))
                    suma_socket.sendall(str(suma_precios).encode())

                    suma_calculada = suma_socket.recv(1024)
                    suma_socket.close()

                client_socket.sendall(str(float(suma_calculada)).encode())

        except Exception as e:
            print(f"Error al manejar la conexión del cliente: {e}")

    def apply_local_iva(self, productos):
        for producto in productos:
            producto['precio'] *= 1.19
        return productos

if __name__ == "__main__":
    copia_server = CopiaServer(12356, 12346, 12347)
    copia_server.main()
