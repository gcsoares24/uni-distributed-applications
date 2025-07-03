import requests
import json

VERIFY = 'root.pem'
CERT = ('cli.crt', 'cli.key')

def error(error_response, status_code):
    print(error_response["error"] + f" Status code: {status_code}")

def message(r):
    response_data = r.json()
    if response_data.get("error"):
        error(r.json(), r.status_code)
    elif response_data.get("json"):
        print('***')
        print(json.dumps(response_data.get("json"), indent=4, ensure_ascii=False))
        if(response_data.get("not_found")):
            print('The following assets were not found:')
            for item in response_data.get("not_found"):
                print(f"    - {item}")
        print('***')
    else:
        print('***')
        print(response_data.get("success"))
        print('***')

def createUser(BASE_URL):
    data = {'balance':0, 'is_manager':0}
    r = requests.post(f'{BASE_URL}/login', json=data, verify=VERIFY, cert=CERT)
    if r.status_code == 201:
        response_data = r.json()
        client_id = response_data.get("location", "").split("/")[-1]
        print(f"New client ID: {client_id}")
        print('***')
        return client_id
    else:
        print(f"Failed to create user. Status code: {r.status_code}")
        print(r.text)
        return None

def user(BASE_URL, client_id):
    VERIFY = 'root.pem'
    CERT = ('cli.crt', 'cli.key')
    r = requests.get(f'{BASE_URL}/user/{client_id}', verify=VERIFY, cert=CERT)
    if r.status_code == 200:
        print('***')
        response_data = r.json()
        if int(client_id) != 0:
            print(f'    User balance: {response_data.get("balance")}')
            assets = response_data.get("assets", [])
            if assets:
                print("    User assets:")
                for asset in assets:
                    print(f"        - {asset['asset_symbol']}: {asset['quantity']}")
            else:
                print("    You have no assets.")
        else:
            print("    You are the manager.")
        print('***')
    else:
        error(r.json(), r.status_code)
        return 'None'

def addAsset(BASE_URL, name:str, symbol:str,price:float,available_supply:int):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    data = {
        "symbol": symbol,
        "name": name,
        "price": price,
        "available_supply": available_supply
    }
    r = requests.post(f'{BASE_URL}/asset',  json=data, headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def getAsset(BASE_URL, symbol):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    r = requests.get(f'{BASE_URL}/asset/{symbol}', headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def assetSet(BASE_URL, assets):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    r = requests.get(f'{BASE_URL}/assetset/{assets}', headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def buyAsset(BASE_URL, symbol, quantity, client_id):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    data = {'symbol':symbol, 'quantity':quantity, 'client_id':client_id}
    r = requests.post(f'{BASE_URL}/buy',json = data, headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def sellAsset(BASE_URL, symbol, quantity, client_id):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    data = {'symbol':symbol, 'quantity':quantity, 'client_id':client_id}
    r = requests.post(f'{BASE_URL}/sell',json = data, headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def deposit(BASE_URL, client_id, quantity):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    data = {'client_id': client_id, 'quantity': quantity}

    r = requests.post(f'{BASE_URL}/deposit',json = data, headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def withdraw(BASE_URL, client_id, quantity):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    data = {'client_id': client_id, 'quantity': quantity}
    r = requests.post(f'{BASE_URL}/withdraw',json = data, headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def transactions(BASE_URL, start, end):
    headers = {'Content-Type': 'application/vnd.collection+json'}
    r = requests.get(f'{BASE_URL}/transactions/{start};{end}', headers=headers, verify=VERIFY, cert=CERT)
    message(r)

def redirectCommand(BASE_URL, command, client_id):
    command_split = command.split(";")
    try:
        if 'ADD_ASSET' in command:
            if float(command_split[3]) > 0.0 and int(command_split[4]) > 0:
                addAsset(BASE_URL, command_split[1], command_split[2], float(command_split[3]), int(command_split[4]))
            else:
                print("Invalid input. Price and available supply must be greater than 0.")
        elif 'ASSETSET' in command:
            when = len("ASSETSET;")
            assetSet(BASE_URL, command[when:])
        elif 'ASSET' in command:
            getAsset(BASE_URL, command_split[1])
        elif 'BALANCE' in command:
            user(BASE_URL, client_id)
        elif 'BUY' in command:
            if int(command_split[2]) > 0:
                buyAsset(BASE_URL, command_split[1], int(command_split[2]), client_id)
            else:
                print("Invalid quantity. Quantity must be greater than 0.")
        elif 'SELL' in command:
            if int(command_split[2]) > 0:
                sellAsset(BASE_URL, command_split[1], int(command_split[2]), client_id)
            else:
                print("Invalid quantity. Quantity must be greater than 0.")
        elif 'DEPOSIT' in command:
            if float(command_split[1]) > 0:
                deposit(BASE_URL, client_id, float(command_split[1]))
            else:
                print("Invalid quantity. Quantity must be greater than 0.")
        elif 'WITHDRAW' in command:
            if float(command_split[1]) > 0:
                withdraw(BASE_URL, client_id, float(command_split[1]))
            else:
                print("Invalid quantity. Quantity must be greater than 0.")
        elif 'TRANSACTIONS' in command:
            transactions(BASE_URL, command_split[1], command_split[2])
        elif 'USER' in command:
            if int(command_split[1]) == 0:
                print("You cannot view the root user.")
            elif int(command_split[1]) > 0:
                user(BASE_URL, command_split[1])
            else:
                print("Invalid user ID. User ID must be a positive integer.")
        else:
            print("Invalid command.")
    except Exception as e:
        print("Invalid command.")
