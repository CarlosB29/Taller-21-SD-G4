import zmq

def descuento():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5690")

    while True:
        # Recibir el total y la edad desde el broker
        total_pagar, edad = socket.recv_pyobj()

        # Aplicar descuento si la edad es mayor a 60 años
        if edad > 60:
            descuento = total_pagar * 0.2
            total_con_descuento = total_pagar - descuento
            premios = ["Premio A", "Premio B", "Premio C"]

            # Enviar el total con descuento y la lista de premios al broker
            socket.send_pyobj((total_con_descuento, premios))
        else:
            # Enviar el total sin descuento al broker
            socket.send_pyobj((total_pagar, None))

if __name__ == "__main__":
    descuento()
