"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from coincenter_data import Asset, User
from typing import Dict,List

class CoinCenterSkeleton:
    def __init__(self):
        self.assets:Dict[str, Asset] = {}
        self.users:Dict[int, User] = {}
        

    
    def handle_request(self, request):
        user_id = int(request[-1])
        
        if user_id not in self.users:
            this_user = User(user_id)
            self.users[user_id] = this_user
            
            
        command = int(request[0])
        if command == 10:
            return self.handle_add_asset(request[1:])
        elif request[0] == 20 or command == 50:
            return self.handle_get_all_assets(command)
        elif command == 30:
            return self.handle_remove_asset(request[1:])
        elif command == 60:
            return self.handle_get_assets_balance(request[1:])
        elif command == 70:
            return self.handle_buy(request[1:])
        elif command == 80:
            return self.handle_sell(request[1:])
        elif command == 100:
            return self.handle_deposite(request[1:])
        elif command == 110:
            return self.handle_withdraw(request)
        elif command == 90 or command == 40:
            return self.handle_exit(command)

        
    def handle_add_asset(self, args):
        if args[1] in self.assets:
            return [False, args[1]]
        
        asset = Asset(args[1], args[0], float(args[2]), int(args[3]))
        self.assets[args[1]] = asset
        return [11, True]
    
    
    def handle_get_all_assets(self, args):
        if not self.assets:
            return [args + 1, False]
        response = [args + 1, True]
        
        for asset in self.assets.values():
            response.append(asset.__str__())
        
        return response
    
        
    def handle_get_assets_balance(self, args):
        user_id = args[-1]
        user = self.users[user_id]
        if not user.holdings and                                                                                                                                                                                                                                                                                                                                                                                                user.balance == 0:
                return [args[0] + 1, False]
        
        
        assets = [60 + 1, True, user.balance]
        
        for asset_symbol in user.holdings:
            assets.append(f"{asset_symbol};{user.holdings[asset_symbol]}")
        
        return assets


    def handle_buy(self, args):
        user_id = args[-1]
        asset_symbol = args[0]
        
        quantity = float(args[1])
        
        
        if asset_symbol not in self.assets:
            return [71, False]
        
        
        asset = self.assets[asset_symbol]
        user = self.users[user_id]
        
        
        enough_balance = (asset.check_availability(quantity) and
            (user.balance - (asset.price * quantity)) >= 0)
        
        
        if not enough_balance:
            return [71, False]
        
        
        self.handle_withdraw(["nada", asset.price * quantity, user_id])
        if asset_symbol not in user.holdings:
            user.holdings[asset_symbol] = float(quantity)
        else:
            user.holdings[asset_symbol] += quantity
        
        asset.available_supply -= quantity
        return [71, True]
        
        

    def handle_deposite(self, args):
        
        user_id = args[-1]
        amount = float(args[0])

         
         
        self.users[user_id].balance += amount
        return [101, True]


    def handle_sell(self, args):
        user_id = args[-1]
        asset_symbol = args[0]
        quantity = args[1]
        
        if asset_symbol not in self.users[user_id].holdings:
            return [81, False]
        
        asset = self.assets[asset_symbol]
        user = self.users[user_id]
        
        
        if user.holdings[asset_symbol] >= quantity:
            
            user.holdings[asset_symbol] -= quantity
            self.handle_deposite([asset.price * quantity, user_id])
            asset.increase_quntity(quantity)
            if user.holdings[asset_symbol] == 0.0:
                del user.holdings[asset_symbol]

            return [81, True]
        
        else:
            return [81, False]
    
    
    def handle_exit(self, args):
        return [args + 1, True]

    
    def handle_remove_asset(self, args):
        asset_symbol = args[0]
        
        for user in self.users.values():
            if asset_symbol in user.holdings:
                return [31, False]

        if asset_symbol not in self.assets:
            return [31, False]
        
        del self.assets[asset_symbol]
        return [31, True]


    def handle_withdraw(self, args):
        user_id = args[-1]
        amount = float(args[1])
        
        
        if self.users[user_id].balance >= amount:
            self.users[user_id].balance -= amount
            return [111, True]
        