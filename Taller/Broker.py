import zmq

def broker():
    context = zmq.Context()
    frontend = context.socket(zmq.ROUTER)
    backend = context.socket(zmq.DEALER)

    frontend.bind("tcp://*:5559")
    backend.bind("tcp://*:5560")

    descuento_socket = context.socket(zmq.REQ)
    descuento_socket.connect("tcp://localhost:5690")

    # Ciclo principal del broker
    while True:
        try:
            zmq.proxy(frontend, backend)
        except zmq.ContextTerminated:
            break

if __name__ == "__main__":
    broker()
