import zmq

def broker():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)  # Maneja las conexiones de los clientes, actúa como enrutador
    backend = context.socket(zmq.DEALER)  # Socket maneja la conexión al servidor, actúa como distribuidor

    frontend.bind("tcp://*:5559")  # Puerto que recibe el mensaje del cliente.
    backend.bind("tcp://*:5560")  # Puerto que recibe los mensajes del servidor.

    # Creación del socket con el nodo Descuento
    descuento_socket = context.socket(zmq.REQ)
    descuento_socket.connect("tcp://localhost:5690")

    # Ciclo principal del broker
    poller = zmq.Poller()
    poller.register(frontend, zmq.POLLIN)
    poller.register(backend, zmq.POLLIN)

    while True:
        socks = dict(poller.poll(10000))  # Espera 10 segundos por eventos

        if frontend in socks:
            # Enviar mensaje desde el cliente al servidor
            mensaje = frontend.recv_multipart()
            backend.send_multipart(mensaje)

        if backend in socks:
            # Enviar mensaje desde el servidor al cliente
            mensaje = backend.recv_multipart()
            frontend.send_multipart(mensaje)

if __name__ == "__main__":
    broker()
