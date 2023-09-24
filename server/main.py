from utils import log, Socket, Rsa
import time

def handle_disconnection(client_info):
    global my_socket
    for connection in my_socket.connections:
        if connection is not client_info:
            connection.send(f'{my_socket.connections[client_info]["name"]} has left the chat.\n'.encode())

def handle_connection(client):
    global my_socket
    client.send(b'Welcome to the server!\nPress CTRL + C to close the connection.\nEnter your name: ')
    name = client.recv(1024).decode().strip()
    my_socket.connections[client] = {'name': name, 'room': 'default'}  # Add 'room' to the dictionary
    for connection in my_socket.connections:
        if connection is not client:
            connection.send(f'{name} has joined the chat.\n'.encode())
    return f'Welcome, {name}!\n'.encode()

def handle_data(client, data):
    global my_socket
    log.info(f'Received data: {data} from {client.getpeername()}')
    client_info = my_socket.connections[client]
    name = client_info['name']
    room = client_info['room']

    if data == b'/help\n':
        help_lines = [
            '------------------',
            '/help - displays this message',
            '/name <name> - changes your name to <name>',
            '/room <room_name> - changes your room to <room_name> or shows the current room if no argument is given',
            '/pm <name> <message> - sends a private message to <name> with the contents <message>',
            '/users - list all connected users',
            '/rooms - list all rooms',
            '------------------\n'
        ]
        return '\n'.join(help_lines).encode()
    elif b'/name' in data:
        new_name = data.decode().strip().split(' ')[1]
        old_name = client_info['name']
        client_info['name'] = new_name
        for connection in my_socket.connections:
            if connection is not client:
                connection.send(f'{old_name} has changed their name to {new_name}.\n'.encode())
        return f'Your name has been changed to {new_name}.\n'.encode()
    
    elif b'/room' in data and data != b'/rooms\n':
        try:
            new_room = data.decode().strip().split(' ')[1]
            if new_room == room:
                raise IndexError
            client_info['room'] = new_room
            for connection in my_socket.connections:
                if connection is not client:
                    connection.send(f'{name} has moved to room {new_room}.\n'.encode())
            return f'You are now in room {new_room}.\n'.encode()
        except IndexError:
            return f'You are currently in room {room}.\n'.encode()
        
    elif b'/pm' in data:
        data = data.decode().strip().split(' ')
        recipient_name = data[1]
        message = ' '.join(data[2:])
        for connection, connection_info in my_socket.connections.items():
            if connection_info['name'] == recipient_name:
                connection.send(f'PM from {name}: {message}\n'.encode())
                return f'PM sent to {recipient_name}.\n'.encode()
        return f'User {recipient_name} not found.\n'.encode()
    
    elif data == b'/users\n':
        users_in_room = [connection_info['name'] for connection, connection_info in my_socket.connections.items() if connection_info['room'] == room]
        return ('Current users in room ' + room + ': ' + ', '.join(users_in_room) + '\n').encode()
    
    elif data == b'/rooms\n':
        rooms = set([connection_info['room'] for connection, connection_info in my_socket.connections.items()])
        return ('Current rooms: ' + ', '.join(rooms) + '\n').encode()

    for connection, connection_info in my_socket.connections.items():
        if connection_info['room'] == room and connection is not client:
            connection.send(f'{name}: {data.decode()}'.encode())
    return None

log.info('Press enter to close the server at any time.')
my_socket = Socket(14201, handler=handle_data, connection_handler=handle_connection, disconnect_handler=handle_disconnection)
input()
my_socket.close()
log.error('Server closed.')
