"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from typing import Dict,List


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


class User():
    def __init__(self, id):
        self.id = id    
        self.balance = 100
        self.holdings:Dict[str,float] = {}