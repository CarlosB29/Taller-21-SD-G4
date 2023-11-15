import zmq

def suma_node():
    #Se crea un contexto de ZeroMQ y se vincula un socket REP al puerto 5580 para recibir mensajes del servidor.
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5580")

    # Ciclo principal del SumaNode
    while True:
        try:
            # Recibir la lista de productos con IVA del servidor
            message = socket.recv_pyobj()

            # Sumar los precios
            total_response = sum([producto['precio'] for producto in message])

            # Mostrar el total con la suma realizada en SumaNode
            print(f"\nTotal a pagar (con suma en SumaNode): ${total_response}")

            # Enviar el total al servidor
            socket.send_pyobj(total_response)
        except zmq.ContextTerminated:
            #En caso de que el contexto de ZeroMQ se termine, se sale del bucle.
            break

if __name__ == "__main__":
    suma_node()
