import socket
import concurrent.futures
import threading

server_ip = '192.168.0.13'
server_port = 14201

def scan_server(ip):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((ip, server_port))
        print(f'Found server at {ip}.')
    except (ConnectionRefusedError, TimeoutError):
        print(f'Connection to {ip} failed.')
        return None

if server_ip == None:
    print('Scanning for server...')
    
    # Generate a list of IP addresses to scan
    ip_addresses = [f'192.168.{i}.{j}' for i in range(256) for j in range(256)]
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(scan_server, ip_addresses))
    
    # Filter out None values (failed connections) and get the first result
    server_ip = next((ip for ip in results if ip is not None), None)
    
    if server_ip:
        print(f'Found server at {server_ip}.')
    else:
        print('Server not found on the local network.')

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