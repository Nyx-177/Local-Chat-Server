from utils import log, Socket, Rsa
import time

def handle_disconnection(client_info):
    global my_socket
    for connection in my_socket.connections:
        if connection is not client_info:
            connection.send(f'{my_socket.connections[client_info]} has left the chat.\n'.encode())

def handle_connection(client):
    global my_socket
    client.send(b'Welcome to the server!\nPress CTRL + C to close the connection.\nEnter your name: ')
    name = client.recv(1024).decode().strip()
    my_socket.connections[client] = name
    for connection in my_socket.connections:
        if connection is not client:
            connection.send(f'{name} has joined the chat.\n'.encode())
    return f'Welcome, {name}!\n'.encode()

def handle_data(client, data):
    global my_socket
    log.info(f'Received data: {data} from {client.getpeername()}')
    for connection in my_socket.connections:
        if connection is not client:
            connection.send(f'{my_socket.connections[client]}: {data.decode()}'.encode())
    return None

log.info('Press enter to close the server at any time.')
my_socket = Socket(14201, handler=handle_data, connection_handler=handle_connection, disconnect_handler=handle_disconnection)
input()
my_socket.close()
log.error('Server closed.')
