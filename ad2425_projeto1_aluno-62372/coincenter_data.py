"""
Aplicações Distribuídas - Projeto 1 - coincenter_data.py
Números de aluno: 62372
"""
from typing import Dict,List
from abc import ABC, abstractmethod

class Asset:
    def __init__(self, symbol:str, name:str, price:float, available_supply:int):
        self.symbol = symbol
        self.name = name
        self.price = price
        self.available_supply = available_supply
    
    def __str__(self):
        return f"{self.name};{self.symbol};{self.price};{self.available_supply}"



    def check_availability(self, quantity:int) -> bool:
        return (quantity <= self.available_supply) and (quantity != 0)
    
    def decrease_quntity(self, quantity:int) -> bool:
        if(self.check_availability(quantity)):
            self.available_supply -= quantity
            return True
        
        return False
     
    def increase_quntity(self, quantity):
        self.available_supply += quantity

class AssetController:
    assets:Dict[str, Asset] = {}


    @staticmethod
    def list_all_assets()->str:
        string = "ALL_ASSETS;"
        
        for asset in AssetController.assets.values():
            string += asset.__str__() + ":"
        
        return string[:len(string)]
    
    @staticmethod
    def remove_asset(symbol:str):
        if symbol in AssetController.assets:
            del AssetController.assets[symbol]

    @staticmethod
    def add_asset(symbol:str,name:str,price:float,available_supply:int):
        exists = False
        for item in AssetController.assets.keys():
            if item == symbol:
                exists = True
        if not exists:            
            asset = Asset(symbol, name, price, available_supply)
            AssetController.assets[symbol] = asset



class Client(ABC):
    def __init__(self, id):
        self.id = id
    
    @abstractmethod
    def process_request(self, _):
        pass
    
class User(Client):
    
    def __init__(self, user_id):
        super().__init__(user_id)
        self.balance:float = 0.0
        self.holdings:Dict[str, float] = {}

    def __str__(self):
        title_line = f"id: {self.id}"
        balance_line = f"Balance: {self.balance}"
        holdings_lines = []
        
        for symbol, quantity in self.holdings.items():
            holdings_lines.append(f"{symbol}: {quantity}")
        
        max_width = max(len(title_line), len(balance_line), max((len(line) for line in holdings_lines), default=0))
        separator = " " + "_" * (max_width + 2)
        divider = "~" * max_width
        
        title_centered = title_line.center(max_width)
        balance_line_centered = balance_line.center(max_width)
        
        holdings_lines_centered = ""
        for line in holdings_lines:
            holdings_lines_centered += f"| {line.center(max_width)} |\n"
        
        return f"{separator}\n| {title_centered} |\n| {balance_line_centered} |\n {divider}\n{holdings_lines_centered}{separator}"
    
    def buy_asset(self, asset_symbol:str, quantity:float) -> bool:
        if asset_symbol not in AssetController.assets:
            return False
        
        asset = AssetController.assets[asset_symbol]
        
        enoughBalance = (asset.check_availability(quantity) and
           (self.balance - (asset.price * quantity)) > 0)
        
        if not enoughBalance:
            return False
        
        
        self.withdraw(asset.price * quantity)
        if(asset_symbol not in self.holdings):
            self.holdings[asset_symbol] = quantity
        else:
            self.holdings[asset_symbol] += quantity
        
        asset.available_supply -= quantity
        return True


    def sell_asset(self, asset_symbol:str, quantity:float) -> bool:
        if asset_symbol not in AssetController.assets:
            return False
        
        asset = AssetController.assets[asset_symbol]
        
        self.deposite(asset.price * quantity)
        
        if(asset_symbol in self.holdings) and self.holdings[asset_symbol] >= quantity:
            self.holdings[asset_symbol] -= quantity
        else:
            return False
            
        return True
        

    def deposite(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        self.balance -= amount
    
    def process_request(self, request) -> str:
        
        request_type = request[0]
        action = False

        if request_type == "GET_ASSETS_BALANCE":
            if self.balance == 0 and not self.holdings:
                return "BALANCE;€ 0"
            string = f"BALANCE;€\n{self.balance};"
            for i, (key, value) in enumerate(self.holdings.items()):
                asset = AssetController.assets[key]
                string += f"{asset.name};{asset.symbol};{value}"
                if i < len(self.holdings) - 1:
                    string += ":"
            return string
 
        elif request_type == "GET_ALL_ASSETS":
            if AssetController.list_all_assets():
                return AssetController.list_all_assets()
        
        elif request_type == "BUY":
            action = self.buy_asset(request[1], float(request[2]))
            
        elif request_type == "SELL":
            action = self.sell_asset(request[1], float(request[2]))
            
        elif request_type == "DEPOSIT":
            self.deposite(float(request[1].split()[0]))
            return "OK"
        
        elif request_type == "WITHDRAW":
            value = float(request[1].split()[0])
            if self.balance >= value:
                self.withdraw(float(request[1].split()[0]))
            return "OK"
        
        
        if action:
            return "OK"
        
        #Any anomality:
        return "NOK"        
            

class Manager(Client):
    def __init__(self, user_id):
        super().__init__(user_id)

    def process_request(self, request):
        request_type = request[0]

        if request_type == "ADD_ASSET":
            before = len(AssetController.assets)
            AssetController.add_asset(request[2], request[1], float(request[3]), int(request[4]))
            if before != len(AssetController.assets):    
                return f"OK;{request[2]}"    

        
        elif request_type == "GET_ALL_ASSETS":
            if AssetController.list_all_assets():
                return AssetController.list_all_assets()
            
        elif request_type == "REMOVE_ASSET":
            for item in AssetController.assets.keys():
                if item == request[1]:
                    AssetController.remove_asset(request[1])
                    return f"OK;{request[1]}" 
        
        return "NOK"

        
class ClientController:
    clients:Dict[int,Client] = {0:Manager(0)}
    @staticmethod
    def process_request(request:str)->str:
        ### código ###
        request = request.split(";")
        client_id = int(request[-1])
        if client_id not in ClientController.clients:
            ClientController.clients[client_id] = User(client_id)
        
        return ClientController.clients[client_id].process_request(request[:-1])
