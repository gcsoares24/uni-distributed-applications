"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
import sys
from coincenter_utils import *
import datetime
from kazoo.client import KazooClient

zh = KazooClient()
zh.start()

zh.ensure_path('/assets')

def show_manager_menu():
    title_line = f"MANAGER MENU"
    
    commands = [
    "ADD_ASSET............Add a new cryptocurrency.",
    "ASSET............Get an asset based on the asset’s Symbol.",
    "ASSETSET.............View assets by their symbols.",
    "TRANSACTIONS............View all transactions within a time range.",
    "USER............Get a user’s balance and assets.",
    "EXIT........................Close the program."
    ]
    
    commands_description = [
    "ADD_ASSET;asset_name;asset_Symbol;price;available_supply",
    "ASSET;asset_symbol",
    "ASSETSET;asset_symbol1;asset_symbol2;...;asset_symbolx",
    "TRANSACTIONS;START_RANGE;END_RANGE",
    "USER;user_id",
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
    "ASSET............Get an asset based on the asset’s Symbol.",
    "ASSETSET.............View assets by their symbols.",
    "BALANCE.............View your balance and assets.",
    "BUY...........................Purchase a cryptocurrency.",
    "SELL..............................Sell a cryptocurrency.",
    "DEPOSIT.......................Add funds to your account.",
    "WITHDRAW...............Withdraw funds from your account.",
    "EXIT........................Close the program."
    ]
    
    commands_description = [
    "ASSET;asset_symbol",
    "ASSETSET;asset_symbol1;asset_symbol2;...;asset_symbolx",
    "BALANCE",
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


def is_non_numeric_string(s):
    return isinstance(s, str) and not s.isdigit() and any(c.isalpha() for c in s)

def is_number(s):
    try:
        float(s)
        return True
    except:
        return False
    
    
def is_valid_command(command, user_id):
    commands = {
        "ASSET": 2,           # ASSET;asset_symbol
        "ADD_ASSET": 5,        # ADD_ASSET;asset_name;asset_Symbol;price;available_supply
        "BALANCE": 1,         # BALANCE
        "BUY": 3,             # BUY;asset_symbol;quantity
        "SELL": 3,            # SELL;asset_symbol;quantity
        "DEPOSIT": 2,         # DEPOSIT;amount
        "WITHDRAW": 2,        # WITHDRAW;amount
        "EXIT": 1,            # EXIT
        "TRANSACTIONS": 3,    # TRANSACTIONS;START_RANGE;END_RANGE
        "USER": 2             # USER;user_id
    }
    valid_user = ["ASSET", "ASSETSET", "BALANCE", "BUY", "SELL", "DEPOSIT", "WITHDRAW", "EXIT"]
    valid_manager = ["ASSET", "ADD_ASSET", "ASSETSET", "TRANSACTIONS", "USER", "EXIT"]

    splitCommand = command.strip().split(";")
    this_comm = splitCommand[0].upper()

    if this_comm != "ASSETSET":
        # Check command exists and argument count
        if this_comm not in commands or len(splitCommand) != commands[this_comm]:
            return False

        # Check user/manager permissions
        if user_id == 0 and this_comm not in valid_manager:
            return False
        elif user_id != 0 and this_comm not in valid_user:
            return False



    # Argument validation per command
    if this_comm == "ASSET":
        return is_non_numeric_string(splitCommand[1])
    elif this_comm == "ADD_ASSET":
        asset_name = splitCommand[1]
        asset_symbol = splitCommand[2]
        price = splitCommand[3]
        available_supply = splitCommand[4]
        return (is_non_numeric_string(asset_name) and is_non_numeric_string(asset_symbol)
                and is_number(price) and is_number(available_supply))
    elif this_comm == "ASSETSET":
        symbols = splitCommand[1:]
        return all(is_non_numeric_string(sym) for sym in symbols)
    elif this_comm == "BUY" or this_comm == "SELL":
        asset_symbol = splitCommand[1]
        quantity = splitCommand[2]
        return is_non_numeric_string(asset_symbol) and is_number(quantity)
    elif this_comm == "DEPOSIT" or this_comm == "WITHDRAW":
        amount = splitCommand[1]
        return is_number(amount)
    elif this_comm == "USER":
        return is_number(splitCommand[1])
    elif this_comm == "TRANSACTIONS":
        try:
            datetime.datetime.fromisoformat(splitCommand[1])
            datetime.datetime.fromisoformat(splitCommand[2])
            return True
        except:
            return False
    elif this_comm == "BALANCE" or this_comm == "EXIT":
        return True

    return False


previous_children = set()
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_flask.py server_ip server_port")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    if server_port <= 0:
        print("Error: server_port must be a positive number greater than 0.")
        sys.exit(1)

    BASE_URL = 'https://' + server_ip + ":" + str(server_port)

    # Start user
    user_id = -1
    while user_id == -1:
        has_account = input("To login use:       LOGIN;user_id\n>>>")
        if "LOGIN" in has_account and len(has_account.split(";")) == 2:
            user_id = has_account.split(";")[1]
            
            if is_number(user_id) and float(user_id).is_integer() and int(user_id) >= 0:
                
                try:
                    exists = user(BASE_URL, user_id)
                    if exists == 'None':
                        print("\nCreating new user....")
                        user_id = createUser(BASE_URL)
                except Exception as e:
                    print(f"Error connecting to the server: {e}")
                    break
            else:
                user_id = -1
                print("The id has to be a integer!")
        else:
            print("WRONG COMMAND! USE:    LOGIN;user_id")
    
    if user_id == -1:
        sys.exit(1)

    if int(user_id) == 0:
        menu = show_manager_menu
    else:
        @zh.ChildrenWatch('/assets')
        def watch_children(children):
            global previous_children
            current_children = set(children)
            new_children = current_children - previous_children
            if new_children:
                print("\n***")
                print("New Asset has been added by an Administrator: %s" % list(new_children)[0])
                print("***")
                print("command V ")

            previous_children = current_children
            
        menu = show_user_menu

    menu()
    while True:
        try:
            command = input("command > ")
            if command.upper() == "EXIT":
                break
            else:
                if is_valid_command(command, int(user_id)):
                    try:
                        redirectCommand(BASE_URL, command, user_id)
                    except Exception as e:
                        print(f"Error executing command: {e}")
                        break
                else:
                    print("invalid command")
        except Exception as e:
            print(f"Unexpected error: {e}")
            break
    
    # Finalizar o cliente Kazoo
    zh.stop()
    zh.close()



if __name__ == "__main__":
    main()