import socket
import pickle
from datetime import datetime
from Producto import Producto  # Ajusta el nombre de importación

def crear_lista_productos():
    productos = []
    cantidad = int(input("Ingrese la cantidad de productos que desea agregar: "))
    for _ in range(cantidad):
        nombre = input("Nombre del producto: ")
        categoria = input("Categoría del producto: ")
        precio = float(input("Precio del producto: "))
        productos.append(Producto(nombre, categoria, precio))
    return productos

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(20)
    try:
        # Intenta conectarse al nodo servidor
        client_socket.connect(('localhost', 8891)) #8891
    except socket.timeout:
        # Si hay un timeout, imprime el mensaje

        print("No se pudo conectar al servidor en 20 segundos. Conectándose a CopiaServer...")

        # Intenta conectarse al nodo copia (CopiaServer)
        client_socket.close()
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', 8891))  # 9002

    lista_productos = crear_lista_productos()
    productos_data = pickle.dumps(lista_productos)
    client_socket.sendall(productos_data)

    total_pagar = client_socket.recv(4096).decode()

    client_socket.close()

    print("\nTotal a pagar recibido del servidor o CopiaServer:")
    print(f"${float(total_pagar):.2f}")

if __name__ == "__main__":
    main()
