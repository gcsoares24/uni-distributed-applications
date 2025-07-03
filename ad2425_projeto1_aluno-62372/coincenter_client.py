"""
Aplicações Distribuídas - Projeto 1 - coincenter_client.py
Números de aluno: 62372
"""

import sys
from net_client import *

### código do programa principal ###
def show_manager_menu():
    title_line = f"MANAGER MENU"
    
    commands = [
    "ADD_ASSET............Add a new cryptocurrency.",
    "REMOVE_ASSET..........Remove a cryptocurrency.",
    "GET_ALL_ASSETS......View all cryptocurrencies.",
    "EXIT........................Close the program."
    ]
    
    commands_description = [
    "ADD_ASSET;asset_name;asset_Symbol;price;available_supply",
    "REMOVE_ASSET;asset_symbol",
    "GET_ALL_ASSETS",
    "EXIT"
    ]
   
    
    max_width = max(len(title_line), max((len(line) for line in commands), default=0), max((len(line) for line in commands_description), default=0))
    separator = " " + "_" * (max_width + 2)
    divider = "~" * (max_width + 2)
    
    title_centered = title_line.center(max_width)
    
    manager_menu = ""
    for line in range(len(commands)):
        manager_menu += f"| {commands[line].center(max_width)} |\n"
        manager_menu += f"| {commands_description[line].center(max_width)} |\n"
        manager_menu += f"| {"".center(max_width)} |\n"
    print(f"{separator}\n| {title_centered} |\n|{divider}|\n{manager_menu}{separator}")

def show_user_menu():
    title_line = f"USER MENU"
    commands = [
    "GET_ASSETS_BALANCE..................Check your current balance.",
    "GET_ALL_ASSETS......View all available cryptocurrencies.",
    "BUY...........................Purchase a cryptocurrency.",
    "SELL..............................Sell a cryptocurrency.",
    "DEPOSIT.......................Add funds to your account.",
    "WITHDRAW...............Withdraw funds from your account.",
    "EXIT..................................Close the program."
    ]
    
    commands_description = [
    "GET_ASSETS_BALANCE",
    "GET_ALL_ASSETS",
    "BUY;asset_symbol;quantity",
    "SELL;asset_symbol;quantity",
    "DEPOSIT;amount",
    "WITHDRAW;amount",
    "EXIT"
    ]
    
    max_width = max(len(title_line), max((len(line) for line in commands), default=0), max((len(line) for line in commands_description), default=0))
    separator = " " + "_" * (max_width + 2)
    divider = "~" * (max_width + 2)
    
    title_centered = title_line.center(max_width)
    
    user_menu = ""
    for line in range(len(commands)):
        user_menu += f"| {commands[line].center(max_width)} |\n"
        user_menu += f"| {commands_description[line].center(max_width)} |\n"
        user_menu += f"| {"".center(max_width)} |\n"
    print(f"{separator}\n| {title_centered} |\n|{divider}|\n{user_menu}{separator}")



def main():
    
    
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)


    ### código ###
    # socket creation
    HOST = sys.argv[2]
    PORT = int(sys.argv[3])
    ID = sys.argv[1]
    client_sock = NetClient(ID, HOST, PORT)
    
    #CHOOSE MENU
    
    if ID == "0":
        menu = show_manager_menu
    else:
        menu = show_user_menu
    
    # send ID
    #usar o client_sock.id?
    client_sock.send(ID)
    
    commands = {
    "ADD_ASSET": 5,
    "GET_ALL_ASSETS": 1,
    "REMOVE_ASSET": 2,
    "BUY": 3,
    "SELL": 3,
    "DEPOSIT": 2,
    "WITHDRAW": 2,
    "GET_ASSETS_BALANCE": 1
    }
    
    # rest of the code
    
    try:
        menu()
        while True:
            frase = input('command > ')
            
            notWorks = False                        
            splitFrase = frase.split(";")
            command = splitFrase[0]

            if command not in commands or len(splitFrase) != commands[command]:
                notWorks = True  
            
            if frase == 'EXIT':
                break
            elif notWorks:
                print(f"ERROR: The command {frase} is not correctly formed!")
            else:
                message = f"{frase};{ID}"
                print('Sent sequence: %s' % message)
                client_sock.send(message)
                client_sock.recv()
                print('Received sequence: %s' % client_sock.answer)
                
    finally:
        client_sock.close()  # By any exception, it closes
    client_sock.close()


if __name__ == "__main__":
    main()