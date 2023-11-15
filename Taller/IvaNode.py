import zmq
import time

def iva_node():
    #Se crea un contexto de ZeroMQ y se vincula un socket REP al puerto 5570 para recibir mensajes del servidor.
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5570")

    # Ciclo principal del IvaNode
    while True:
        try:
            # Recibir la lista de productos del servidor
            message = socket.recv_pyobj()

            # Aplicar el IVA a los productos según la categoría
            for producto in message:
                if producto['categoria'] != 'Canasta':
                    producto['precio'] *= 1.19

            # Mostrar la nueva lista con el IVA
            print("\nNueva lista con IVA aplicado en IvaNode:")
            for producto in message:
                print(producto)

            # Enviar la lista con IVA al servidor
            socket.send_pyobj(message)
#En caso de que el contexto de ZeroMQ se termine, se sale del bucle.
        except zmq.ContextTerminated:
            break

if __name__ == "__main__":
    iva_node()
