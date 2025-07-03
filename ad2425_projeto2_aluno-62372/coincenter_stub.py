"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from net_client import NetClient

class CoinCenterStub:
    def __init__(self, user_id,server_ip,server_port):
        self.id = user_id
        self.net_client = NetClient(server_ip, server_port)


    def handle_command(self, command):
        response = None
        command_parts = command.split(";")
    
        if command_parts[0] == "ADD_ASSET":
            response = self.add_asset(command_parts[1], command_parts[2], float(command_parts[3]), float(command_parts[4]))
        elif command_parts[0] == "REMOVE_ASSET":
            response = self.remove_asset(command_parts[1])
        elif command_parts[0] == "GET_ALL_ASSETS":
            response = self.get_all_assets()
        elif command_parts[0] == "BUY":
            response = self.buy(command_parts[1], float(command_parts[2]))
        elif command_parts[0] == "SELL":
            response = self.sell(command_parts[1], float(command_parts[2]))
        elif command_parts[0] == "DEPOSIT":
            response = self.deposite(float(command_parts[1].split(" ")[0]))
        elif command_parts[0] == "WITHDRAW":
            response = self.withdraw(float(command_parts[1].split(" ")[0]))
        elif command_parts[0] == "GET_ASSETS_BALANCE":
            response = self.get_assets_balance()
        elif command_parts[0] == "EXIT":
            response = self.exit()

        return response


    def add_asset(self, asset_name, asset_symbol, asset_price, available_supply):
        request = [10, asset_name, asset_symbol, asset_price, available_supply, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response


    def get_all_assets(self):
        if self.id == 0:
            comm_id = 20
        else:
            comm_id = 50
        request = [comm_id, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response


    def remove_asset(self, asset_symbol):
        request = [30, asset_symbol, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response
    

    def get_assets_balance(self):
        request = [60, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response


    def buy(self, asset_symbol, quantity):
        request = [70, asset_symbol, quantity, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response
    

    def sell(self, asset_symbol, quantity):
        request = [80, asset_symbol, quantity, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response


    def deposite(self, quantity):
        request = [100, quantity, self.id]
        self.net_client.send(request)
         
        response = self.net_client.recv()
        return response


    def withdraw(self, quantity):
        request = [110, quantity, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response


    def exit(self):
        if self.id == 0:
            comm_id = 90
        else:
            comm_id = 40
        request = [comm_id, self.id]
        self.net_client.send(request)
        response = self.net_client.recv()
        return response
