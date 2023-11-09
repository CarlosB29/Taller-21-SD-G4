import socket

def calcular_suma(suma_precios):
    return suma_precios

def handle_client(client_socket):
    try:
        suma_precios = float(client_socket.recv(1024).decode())
        suma_calculada = calcular_suma(suma_precios)

        client_socket.send(str(suma_calculada).encode())

    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    suma_port = 12347
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", suma_port))
    server_socket.listen(5)

    while True:
        client_socket, _ = server_socket.accept()
        handle_client(client_socket)
