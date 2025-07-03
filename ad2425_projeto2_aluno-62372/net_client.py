"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from sock_utils import *

import pickle
import struct

class NetClient:
    def __init__(self, host, port):
        #self.id = id  --> 
        self.host = host
        self.port = port
        self.sock = create_tcp_client_socket(host, port)

    def send(self, data):
        data_bytes = pickle.dumps(data, -1)
        data_size = struct.pack("i", len(data_bytes))
        self.sock.sendall(data_size)
        self.sock.sendall(data_bytes)


    def recv(self):
        self.sock.settimeout(5)
        answer_size_b = b''
        try:

            answer_size_b = self.sock.recv(4)
            answer_size = struct.unpack("i", answer_size_b)[0]
            answer_b = receive_all(self.sock, answer_size)
        except self.sock.timeout as st:
            self.sock.settimeout(None)
            raise TimeoutError("Time limit is done, can't receive more data")

        return  pickle.loads(answer_b)
        
    
    def close(self):
        self.sock.close()