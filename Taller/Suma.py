import socket
import pickle

def calcular_total_con_iva(productos_con_iva):
    total_pagar = sum(producto.precio for producto in productos_con_iva)
    return total_pagar

def main():
    suma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    suma_socket.bind(('localhost', 8890))
    suma_socket.listen(1)

    print("Nodo Suma en espera de conexiones...")

    while True:
        server_socket, addr = suma_socket.accept()
        print(f"Conexión establecida desde {addr}")

        productos_con_iva_data = server_socket.recv(4096)
        productos_con_iva = pickle.loads(productos_con_iva_data)

        print("\nLista de productos con IVA recibida por el nodo Suma:")
        for producto in productos_con_iva:
            print(f"{producto.nombre} - {producto.categoria} - ${producto.precio:.2f}")

        total_pagar = calcular_total_con_iva(productos_con_iva)

        print("\nCalculando total a pagar con IVA en el nodo Suma...")
        print(f"Total a pagar con IVA: ${total_pagar:.2f}")

        server_socket.sendall(pickle.dumps(total_pagar))
        server_socket.close()

        print("Nodo Suma en espera de conexiones...")

if __name__ == "__main__":
    main()
