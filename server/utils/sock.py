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