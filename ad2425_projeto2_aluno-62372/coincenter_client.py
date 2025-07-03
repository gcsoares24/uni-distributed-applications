"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
from coincenter_stub import CoinCenterStub
import sys

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


def is_valid_command(command, command_list):
    commands = {
    "ADD_ASSET": 5,
    "GET_ALL_ASSETS": 1,
    "REMOVE_ASSET": 2,
    "BUY": 3,
    "SELL": 3,
    "DEPOSIT": 2,
    "WITHDRAW": 2,
    "GET_ASSETS_BALANCE": 1,
    "EXIT": 1
    }
    
    splitCommand = command.split(";")
    this_comm = splitCommand[0] 
    if (this_comm not in commands or len(splitCommand) != commands[this_comm]) or this_comm not in command_list:
        return False

    return True

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 coincenter_client.py user_id server_ip server_port")
        sys.exit(1)
        
    user_id = int(sys.argv[1])
    server_ip = sys.argv[2]
    server_port = int(sys.argv[3])

    stub = CoinCenterStub(user_id, server_ip, server_port)

    commands_id_manager = {
        "ADD_ASSET": 10,
        "GET_ALL_ASSETS": 20,
        "REMOVE_ASSET": 30,
        "EXIT": 40
    }
    
    
    commands_id_client = {
        "GET_ALL_ASSETS": 50,
        "GET_ASSETS_BALANCE": 60,
        "BUY": 70,
        "SELL": 80,
        "EXIT": 90,
        "DEPOSIT": 100,
        "WITHDRAW": 110
    }


    if user_id == 0:
        menu = show_manager_menu
        comm_id = commands_id_manager
    else:
        menu = show_user_menu
        comm_id = commands_id_client
    
    
    menu()
    while True:
        try:
            command = input("command > ")
            
            if command.upper() == "EXIT":
                stub.exit()
                break
            else:
                if is_valid_command(command, comm_id):
                    print('Sent sequence: %s' % command)
                    response = stub.handle_command(command)
                    print(f"Received sequence: {response}") 
                else:
                    print("invalid command")
        except Exception as e:
            print(f"Unexpected error: {e}")
            break

if __name__ == "__main__":
    main()