"""
Aplicações Distribuídas - Projeto 1 - coincenter_server.py
Números de aluno: 62372
"""

import sys
import signal
from net_server import *
from coincenter_data import *

### código do programa principal ###
server = None

def handle_shutdown(signum, frame):
    global server
    server.close()
    sys.exit(0)

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)
    
    # socket creation
    global server
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    server = NetServer(server_ip, server_port)
        
    signal.signal(signal.SIGINT, handle_shutdown)
    
    while True:
        # accept new connection
        server.accept()
        conn_socket = server.conn_sock
        addr = server.addr
        logged = False
        
        while True:
            # receive ID
            if not logged:
                server.recv(conn_socket)
                id = server.answer
                ClientController.client_id = int(id)
                print(f"WELCOME TO COINCENTER, id = {id}!\n IP: {addr[0]}| PORT:{addr[1]}")
                logged = True

            # receive and process requests
            server.recv(conn_socket)
            if server.answer == "EXIT":
                print(f"id = {id}, was disconnected!\n IP: {addr[0]}| PORT:{addr[1]}")
                logged = False
                break
            else:
                print('Received sequence: %s' % server.answer)
                answer = ClientController.process_request(server.answer)
                server.send(conn_socket, answer)
                print('Sent sequence: %s' % answer)

if __name__ == "__main__":
    main()