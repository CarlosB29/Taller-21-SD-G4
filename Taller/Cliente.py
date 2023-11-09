import socket
import pickle
import time

class Cliente:
    def __init__(self, server_address, server_port, backup_port):
        self.server_address = server_address
        self.server_port = server_port
        self.backup_port = backup_port

    def main(self):
        connected = False
        while not connected:
            try:
                connected = self.communicate_with_server(self.server_address, self.server_port)
            except Exception as e:
                print(f"No se pudo conectar al servidor principal. Intentando con el servidor de respaldo...")
                time.sleep(2)
                try:
                    connected = self.communicate_with_server(self.server_address, self.backup_port)
                except Exception as ex:
                    print("No se pudo conectar al servidor de respaldo. Verifique la conexión.")
                    break  # Agregamos esta línea para salir del bucle si la conexión de respaldo también falla

    def communicate_with_server(self, server_address, server_port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect((server_address, server_port))
                productos = self.get_productos_from_user()
                data = pickle.dumps(productos)
                s.sendall(data)
                suma_calculada = s.recv(1024)
                print(f"Total a pagar: {float(suma_calculada)}")
                return True  # Indica que la comunicación fue exitosa
            except Exception as e:
                print(f"No se pudo conectar al servidor en el puerto {server_port}. Detalles: {e}")
                return False  # Indica que la conexión falló

    def get_productos_from_user(self):
        productos = []
        cantidad_productos = int(input("Ingrese la cantidad de productos: "))
        for i in range(cantidad_productos):
            nombre = input(f"Ingrese el nombre del producto {i + 1}: ")
            categoria = input(f"Ingrese la categoría del producto {i + 1}: ")
            precio = float(input(f"Ingrese el precio del producto {i + 1}: "))
            producto = {"nombre": nombre, "categoria": categoria, "precio": precio}
            productos.append(producto)
        return productos

if __name__ == "__main__":
    client = Cliente("localhost", 12345, 12356)
    client.main()
