from utils import log, Socket, Rsa
import time

def handle_connection(client):
    global my_socket
    client.send(b'Welcome to the server!\nType "close" to close the connection.\nEnter your name: ')
    name = client.recv(1024).decode().strip()
    my_socket.connections[client] = name
    return f'Welcome, {name}!\n'.encode()

def handle_data(client, data):
    global my_socket
    log.info(f'Received data: {data} from {client.getpeername()}')
    if data == b'close\n':
        return False
    for connection in my_socket.connections:
        if connection is not client:
            connection.send(f'{my_socket.connections[client]}: {data.decode()}'.encode())
    return None

log.info('Press enter to close the server at any time.')
my_socket = Socket(8080, handler=handle_data, connection_handler=handle_connection)
input()
my_socket.close()
log.error('Server closed.')
