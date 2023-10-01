import socket
import threading

server_ip = 'localhost'
server_port = 14201

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))

def listen():
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # print without adding a newline
        print(data.decode(), end='')

threading.Thread(target=listen).start()

while True:
    data = input().encode()
    client_socket.send(data + b'\n')