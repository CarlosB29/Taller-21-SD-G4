import socket
import pickle
from datetime import datetime
import time
from Producto import Producto  # Ajusta el nombre de importación

def calcular_total(productos):
    total = 0
    for producto in productos:
        total += producto.precio
    return total

def connect_to_suma_node(productos_con_iva):
    suma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    suma_socket.settimeout(20)  # Tiempo de espera de 20 segundos

    try:
        suma_socket.connect(('localhost', 8890))
        suma_socket.sendall(pickle.dumps(productos_con_iva))

        total_pagar_data = suma_socket.recv(4096)
        total_pagar = pickle.loads(total_pagar_data)

        suma_socket.close()
        return total_pagar
    except ConnectionRefusedError:
        print("No se pudo conectar al nodo Suma. Calculando total localmente...")
        suma_socket.close()
        return calcular_total(productos_con_iva)
    except socket.timeout:
        print("Tiempo de espera agotado al intentar conectar al nodo Suma. Calculando total localmente...")
        suma_socket.close()
        return calcular_total(productos_con_iva)


def connect_to_iva_node(productos):
    iva_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    iva_socket.settimeout(20)  # Tiempo de espera de 20 segundos

    try:
        iva_socket.connect(('localhost', 8889))
        iva_socket.sendall(pickle.dumps(productos))

        productos_con_iva_data = iva_socket.recv(4096)
        productos_con_iva = pickle.loads(productos_con_iva_data)

        iva_socket.close()
        return productos_con_iva
    except ConnectionRefusedError:
        print("No se pudo conectar al IvaNode. Aplicando IVA localmente...")
        iva_socket.close()
        # Aplicar el IVA localmente antes de retornar
        for producto in productos:
            if producto.categoria.lower() != "canasta":
                producto.precio *= 1.19  # Aplica un 19% de impuestos
        return productos
    except socket.timeout:
        print("Tiempo de espera agotado al intentar conectar al IvaNode. Aplicando IVA localmente...")
        iva_socket.close()
        # Aplicar el IVA localmente antes de retornar
        for producto in productos:
            if producto.categoria.lower() != "canasta":
                producto.precio *= 1.19  # Aplica un 19% de impuestos
        return productos


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8891))
    server_socket.listen(1)

    print("Copia Servidor en espera de conexiones...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión establecida desde {addr}")

        productos_data = client_socket.recv(4096)
        productos = pickle.loads(productos_data)

        fecha_hora_conexion = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"\nFecha y hora de conexión: {fecha_hora_conexion}")

        print("\nLista de productos recibida:")
        for producto in productos:
            print(f"{producto.nombre} - {producto.categoria} - ${producto.precio:.2f}")

        productos_con_iva = connect_to_iva_node(productos)

        print("\nCalculando total a pagar con IVA...")
        total_pagar = connect_to_suma_node(productos_con_iva)
        print(f"Total a pagar con IVA: ${total_pagar:.2f}")

        client_socket.sendall(str(total_pagar).encode())
        client_socket.close()

        print("Copia Servidor en espera de conexiones...")

if __name__ == "__main__":
    main()
