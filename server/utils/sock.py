class Socket:
    def __init__(self, port, threads=True, handler=print, logging=True):
        from .log import log
        import threading
        import socket

        self.port = port
        self.handler = handler

        self.connections = []
        self.lock = threading.Lock()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', port))
        self.server_socket.listen(5)
        log.info(f'Listening on port {port}')
        if threads:
            self.listen_thread = threading.Thread(target=self.listen)
            self.listen_thread.start()
            log.info('Started listening thread')
    
    def listen(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            connection_thread = threading.Thread(target=self.handle_connection, args=(client_socket,))
            connection_thread.start()

    def handle_connection(self, client_socket):
        with self.lock:
            self.connections.append(client_socket)
        
        client_info = client_socket.getpeername()
        log.info(f'New connection from {client_info or "unknown"}')

        while True:
            try:
                data = client_socket.recv(1024)
            except OSError or ConnectionResetError:
                log.info(f'Connection closed by client {client_info or "unknown"}.')
                break
            if not data:
                log.warn(f'Connection closed by client {client_info or "unknown"} for unknown reason (likely force close).')
                break
            response = self.handler(client_socket, data)
            if response is False:
                self.close_connection(client_socket)
            else:
                client_socket.send(response)
        self.close_connection(client_socket)

    def close_connection(self, client_socket):
        with self.lock:
            try:
                self.connections.remove(client_socket)
            except ValueError:
                pass
        client_socket.close()
    
    def close(self):
        with self.lock:
            for client_socket in self.connections:
                client_socket.close()
            self.connections = []
        self.server_socket.close()
    