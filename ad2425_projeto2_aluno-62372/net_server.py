"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from sock_utils import *

import pickle
import struct

class NetServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = create_tcp_server_socket(host, port, 1)
        self.answer = None


    def accept(self):
        return self.server_socket.accept()


    def recv(self, client_socket):
        answer_size_b = client_socket.recv(4)
        if answer_size_b == b"":
            return None
        answer_size = struct.unpack("i", answer_size_b)[0]
        answer_b =  receive_all(client_socket, answer_size)
        return pickle.loads(answer_b)



    def send(self, client_socket, data):
        data = pickle.dumps(data)
        data_size = struct.pack("i", len(data))
        client_socket.sendall(data_size)
        client_socket.sendall(data)


    def close(self):
        self.server_socket.close()