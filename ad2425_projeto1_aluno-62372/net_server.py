"""
Aplicações Distribuídas - Projeto 1 - net_server.py
Números de aluno: 62372
"""
from sock_utils import *

import pickle
import struct

class NetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = create_tcp_server_socket(host, port, 1)
        self.conn_sock = None
        self.addr = None
        self.answer = None


    def accept(self):
        (self.conn_sock, self.addr) = self.sock.accept()


    def recv(self, client_socket):
        answer_size_b = client_socket.recv(4)
        if answer_size_b:
            answer_size = struct.unpack("i", answer_size_b)[0]
            answer_b = client_socket.recv(answer_size)
            self.answer = pickle.loads(answer_b)
        else:
            self.answer = "EXIT"


    def send(self, client_socket, data):
        data_bytes = pickle.dumps(data, -1)
        data_size = struct.pack("i", len(data_bytes))
        client_socket.sendall(data_size)
        client_socket.sendall(data_bytes)


    def close(self):
        self.sock.close()