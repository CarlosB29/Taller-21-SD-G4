import socket
import pickle

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12346))
    server_socket.listen(5)
    while True:
        with server_socket:
            client_socket, _ = server_socket.accept()
            with client_socket:
                received_data = client_socket.recv(1024)
                producto = pickle.loads(received_data)
                if producto.get_category().lower() != "canasta":
                    nuevo_precio = producto.get_precio() * 1.19
                    producto.set_precio(nuevo_precio)
                    print(f"El precio del producto {producto.get_name()} es: {producto.get_precio()}")
                client_socket.send(pickle.dumps(producto))

if __name__ == "__main__":
    main()
