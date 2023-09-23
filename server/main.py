import socket
import threading

from utils import log, Socket

# Example usage:
def handle_data(client, data):
    log.info(f'Received data: {data} from {client.getpeername()}')
    if data == b'close\n':
        return False
    return data.upper()

log.info('Press enter to close the server at any time.')
my_socket = Socket(8080, handler=handle_data)


input()
my_socket.close()
