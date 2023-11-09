import socket
import pickle
from datetime import datetime
from Producto import Producto  # Ajusta el nombre de importación

def aplicar_iva(productos):
    for producto in productos:
        if producto.categoria.lower() != "canasta":
            producto.precio *= 1.19  # Aplica un 19% de impuestos
    return productos

def main():
    iva_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    iva_socket.bind(('localhost', 8889))
    iva_socket.listen(1)

    print("IvaNode en espera de conexiones...")

    while True:
        server_socket, addr = iva_socket.accept()
        print(f"Conexión establecida desde {addr}")

        productos_data = server_socket.recv(4096)
        productos = pickle.loads(productos_data)

        print("\nLista de productos recibida por IvaNode:")
        for producto in productos:
            print(f"{producto.nombre} - {producto.categoria} - ${producto.precio:.2f}")

        productos_con_iva = aplicar_iva(productos)

        print("\nAplicando IVA...")
        for producto in productos_con_iva:
            print(f"{producto.nombre} - {producto.categoria} - ${producto.precio:.2f}")

        server_socket.sendall(pickle.dumps(productos_con_iva))
        server_socket.close()

        print("IvaNode en espera de conexiones...")

if __name__ == "__main__":
    main()
