import zmq

def cliente():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:5559")

    # Crear lista de productos
    productos = []
    while True:
        nombre = input("Ingrese nombre del producto (o 'fin' para terminar): ")
        if nombre.lower() == 'fin':
            break
        categoria = input("Ingrese la categoría del producto: ")
        precio = float(input("Ingrese el precio del producto: "))

        productos.append({'nombre': nombre, 'categoria': categoria, 'precio': precio})

    # Enviar lista de productos al servidor
    socket.send_pyobj(productos)

    # Recibir el total a pagar desde el servidor
    total = socket.recv_pyobj()

    # Preguntar la edad al usuario
    edad = int(input("¿Cuántos años tienes? "))

    # Si la edad es mayor a 60, solicitar descuento
    if edad > 60:
        print(f"El total a pagar es: ${total:.2f}")
        descuento = input("¿Desea aplicar el descuento? (si/no): ").lower() == "si"

        if descuento:
            descuento_socket = context.socket(zmq.REQ)
            descuento_socket.connect("tcp://localhost:5590")

            # Enviar el total y la edad al nodo de descuento
            descuento_socket.send_pyobj((total, edad))

            # Recibir el total con descuento y la lista de premios
            total_con_descuento, premios = descuento_socket.recv_pyobj()

            print(f"Total con descuento: ${total_con_descuento:.2f}")

            if premios:
                print("Lista de premios:")
                for premio in premios:
                    print(premio)
        else:
            print("No se aplicará el descuento.")
    else:
        print(f"El total a pagar es: ${total:.2f}")

if __name__ == "__main__":
    cliente()
