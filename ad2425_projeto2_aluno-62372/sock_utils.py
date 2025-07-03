"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
import socket as s

def create_tcp_server_socket(address, port, queue_size):
    server = s.socket(s.AF_INET, s.SOCK_STREAM)
    server.setsockopt(s.SOL_SOCKET, s.SO_REUSEADDR, 1)
    server.bind((address, port))
    server.listen(queue_size)
    return server

def create_tcp_client_socket(address, port):
    client = s.socket(s.AF_INET, s.SOCK_STREAM)
    client.connect((address, port))
    return client



def receive_all(socket, length):
    data = b''
    while len(data) < length:
        try:
            packet = socket.recv(length - len(data))
           
            data += packet
        except s.timeout:
            socket.settimeout(None)
            raise TimeoutError("Time limit is done, can't receive more data")
    return data
