"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from coincenter_skel import CoinCenterSkeleton
from net_server import NetServer
import select
import sys
import signal

def handle_shutdown(signum, frame):
    global net_server
    print('Program was interrupted due to keyboard input.')
    if net_server:
        net_server.close()
    sys.exit(0)



def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_server.py server_ip server_port")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    global net_server
    net_server = NetServer(server_ip, server_port)
    signal.signal(signal.SIGINT, handle_shutdown)
    skel = CoinCenterSkeleton()

    sockets = [net_server.server_socket]

    
    while True:
        try:
            ready_to_read, _, _ = select.select(sockets, [], [])

            for sock in ready_to_read:
                if sock is net_server.server_socket:
                    client_sock, addr = net_server.accept()
                    sockets.append(client_sock)
                    print(f"Client {addr} connected")
                else:
                    request = net_server.recv(sock)
                    if request != None:
                        print('Received sequence: %s' % request)
                        response = skel.handle_request(request)
                        net_server.send(sock, response)
                        print('Sent sequence: %s' % response)
                    else:
                        print(f"Client {addr} disconnected")
                        sockets.remove(sock)
                        sock.close()
                        break
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
if __name__ == "__main__":
    main()



