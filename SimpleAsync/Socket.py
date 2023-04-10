import socket
import Errors


class Socket:
    def __init__(self, socket: socket.socket):
        if socket.getblocking():
            raise Errors.BlockingSocket
