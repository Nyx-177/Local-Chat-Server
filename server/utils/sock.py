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
    