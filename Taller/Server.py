import zmq
import time
import logging

# Configuración básica de logging
logging.basicConfig(level=logging.INFO)

def server():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.connect("tcp://localhost:5560")
    logging.info("Servidor esperando un publicador...")

    # Ciclo principal del servidor
    while True:
        iva_socket = context.socket(zmq.REQ)
        suma_socket = context.socket(zmq.REQ)

        try:
            iva_socket.connect("tcp://localhost:5570")
            suma_socket.connect("tcp://localhost:5580")

            # Recibir la lista de productos desde el cliente
            message = socket.recv_pyobj()

            # Mostrar la lista original
            logging.info("Lista de productos recibida:")
            for producto in message:
                logging.info(producto)

            # Intentar aplicar el IVA con IvaNode
            try:
                iva_socket.send_pyobj(message)
                iva_response = iva_socket.recv_pyobj()
            except zmq.Again:
                logging.warning("No se pudo conectar con IvaNode. Aplicando IVA localmente...")
                iva_response = message
                for producto in iva_response:
                    if producto['categoria'] != 'Canasta':
                        producto['precio'] *= 1.19

            # Mostrar la nueva lista con el IVA
            logging.info("\nNueva lista con IVA aplicado:")
            for producto in iva_response:
                logging.info(producto)

            # Intentar realizar la suma con SumaNode
            try:
                suma_socket.send_pyobj(iva_response)
                total_response = suma_socket.recv_pyobj()
            except zmq.Again:
                logging.warning("No se pudo conectar con SumaNode. Realizando la suma localmente...")
                total_response = sum([producto['precio'] for producto in iva_response])

            # Mostrar el total a pagar
            logging.info(f"\nTotal a pagar (con suma): ${total_response}")

            # Enviar el total al cliente
            socket.send_pyobj(total_response)

            logging.info("Servidor esperando un publicador...")

        except Exception as e:
            logging.error(f"Error en el servidor: {e}")

        finally:
            # Cerrar sockets
            try:
                iva_socket.close()
                suma_socket.close()
            except zmq.error.ZMQError as e:
                logging.error(f"Error al cerrar sockets: {e}")

        # Esperar 10 segundos antes de intentar nuevamente la conexión
        time.sleep(10)

if __name__ == "__main__":
    server()
