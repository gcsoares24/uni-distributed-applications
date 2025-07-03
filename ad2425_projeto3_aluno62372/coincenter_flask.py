"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""
import sqlite3
from flask import Flask, request, jsonify, make_response
from setup_db import connect_db
import sys
import datetime
from coincenter_data import *
import ssl

#Kazoo
from kazoo.client import KazooClient

zh = KazooClient()
zh.start()

# Garantir que o nó '/assets/' existe
zh.ensure_path('/assets')

#the rest



app = Flask(__name__)

@app.route('/user/<int:client_id>', methods=["GET"])
def user(client_id=None):
    conn, cursor = connect_db()
    if request.method == "GET":
        # Obter dados do client pelo ID
        client, clientAssets = get_client_money(cursor, client_id)
        
        assets = [{"asset_symbol": asset[0], "quantity": asset[1]} for asset in clientAssets]
        conn.close()
        
        if client:
            return make_response(jsonify({
                "balance": client[2],
                "assets": assets
            }), 200)
        return make_response(jsonify({"error": "Client not found"}), 404)


@app.route('/login', methods=["POST"])
def login():
    conn, cursor = connect_db()
    if request.method == "POST":
        data = request.get_json()
        
        # Insert the new user into the database
        add_client(cursor, data['balance'], data['is_manager'])

        conn.commit()
        client_id = cursor.lastrowid
        conn.close()

        return make_response(jsonify({"location": f"/clients/{client_id}"}), 201)


@app.route('/asset', methods=["POST"])
@app.route('/asset/<string:asset_symbol>', methods=["GET"])
def asset(asset_symbol=None):
    conn, cursor = connect_db()
    if request.method == "POST":
        data = request.get_json()
        if not data or "symbol" not in data or "name" not in data or "price" not in data or "available_supply" not in data:
            conn.close()
            return make_response(jsonify({"error": "Invalid data"}), 400)

        success, error = add_asset(cursor, data["symbol"], data["name"], data["price"], data["available_supply"])
        
        if not success:
            conn.close()
            return make_response(jsonify({"error": "Asset already exists", "details": error}), 400)
        conn.commit()
        asset_name = data["name"]
        conn.close()
        zh.create(f'/assets/{data["name"]}', ephemeral=True)
        return make_response(jsonify({"success": f"Asset {asset_name} added successfully"}), 201)

    if request.method == "GET":
        asset = get_asset(cursor, asset_symbol)
        conn.close()
        if asset:
            return make_response(jsonify({"json": {
                "asset_symbol": asset[0],
                "asset_name": asset[1],
                "value": asset[2],
                "available_quantity": asset[3]
            }}), 200)
        return make_response(jsonify({"error": "Asset not found"}), 404)
    

@app.route('/assetset/<string:asset_symbols>', methods=["GET"])
def assetset(asset_symbols = None):
    conn, cursor = connect_db()
    if request.method == "GET":
        symbols = asset_symbols.split(";")
        assets = get_assets_by_symbols(cursor, symbols)
        conn.close()

        found_symbols = set()
        if assets:
            data = {}
            for asset in assets:
                data[asset[0]] = {
                    "asset_name": asset[1],
                    "value": asset[2],
                    "available_quantity": asset[3]
                }
                found_symbols.add(asset[0])
            response = {"json": data}
            not_found = set(symbols) - found_symbols
            if not_found:
                response["not_found"] = list(not_found)
            return make_response(jsonify(response), 200)
        return make_response(jsonify({"error": "No assets found", "not_found": list(symbols)}), 404)
    


@app.route('/buy', methods=["POST"])
def buy():
    conn, cursor = connect_db()
    if request.method == "POST":
        data = request.get_json()
        symbol = data["symbol"]
        client_id = int(data["client_id"])
        quantity = int(data["quantity"])

        # Get asset price and available quantity
        asset = get_asset_price_and_quantity(cursor, symbol)
        if asset is None:
            conn.close()
            return make_response(jsonify({"error": f"Asset {symbol} not found"}), 404)

        price, avail_quantity = int(asset[0]), int(asset[1])
        if quantity > avail_quantity:
            conn.close()
            return make_response(jsonify({"error": f"Not enough {symbol} to buy!"}), 400)

        # Get client balance
        balance = get_client_balance(cursor, client_id)
        if balance is None:
            conn.close()
            return make_response(jsonify({"error": "Client not found"}), 404)

        total_price = price * quantity
        if balance < total_price:
            conn.close()
            return make_response(jsonify({"error": "Not enough funds to buy!"}), 400)

        # Get client asset quantity
        client_asset = get_client_asset_quantity(cursor, client_id, symbol)
        if client_asset:
            new_quantity = client_asset[0] + quantity
            update_client_asset_quantity(cursor, client_id, symbol, new_quantity)
        else:
            insert_client_asset(cursor, client_id, symbol, quantity)

        new_balance = balance - total_price
        new_asset_quantity = avail_quantity - quantity
        now = datetime.datetime.now().isoformat()
        process_transaction(cursor, client_id, new_balance, symbol, new_asset_quantity, 'BUY', quantity, price, now)

        conn.commit()
        conn.close()
        return make_response(jsonify({"success": f"Bought {quantity} of {symbol} successfully"}), 200)

@app.route('/sell', methods=["POST"])
def sell():
    conn, cursor = connect_db()
    if request.method == "POST":
        data = request.get_json()
        symbol = data["symbol"]
        client_id = int(data["client_id"])
        quantity = int(data["quantity"])

        # Get asset price and available quantity
        asset = get_asset_price_and_quantity(cursor, symbol)
        if asset is None:
            conn.close()
            return make_response(jsonify({"error": f"Asset {symbol} not found"}), 404)

        price, avail_quantity = int(asset[0]), int(asset[1])

        # Get client asset quantity
        client_asset = get_client_asset_quantity(cursor, client_id, symbol)
        if not client_asset:
            conn.close()
            return make_response(jsonify({"error": f"You do not have {symbol} to sell!(CONFLICT)"}), 409)

        user_quantity = client_asset[0]
        if user_quantity < quantity:
            conn.close()
            return make_response(jsonify({"error": f"Not enough {symbol} to sell!(CONFLICT)"}), 409)

        # Get client balance
        balance = get_client_balance(cursor, client_id)
        if balance is None:
            conn.close()
            return make_response(jsonify({"error": "Client not found"}), 404)

        real_value = price * quantity
        new_user_quantity = user_quantity - quantity

        update_client_asset_quantity(cursor, client_id, symbol, new_user_quantity)
        new_balance = balance + real_value
        new_asset_quantity = avail_quantity + quantity
        now = datetime.datetime.now().isoformat()
        process_transaction(cursor, client_id, new_balance, symbol, new_asset_quantity, 'SELL', quantity, price, now)

        conn.commit()
        conn.close()
        return make_response(jsonify({"success": f"You sold {quantity} of {symbol} successfully"}), 200)
    
@app.route('/deposit', methods=["POST"])
def deposit():
    conn, cursor = connect_db()
    if request.method == "POST":
        data = request.get_json()
        client_id = data['client_id']
        amount = float(data['quantity'])

        # Get client balance using helper function
        balance = get_client_balance(cursor, client_id)
        if balance is None:
            conn.close()
            return make_response(jsonify({"error": "Client not found"}), 404)

        new_balance = balance + amount

        # Update client balance using helper function
        update_client_balance(cursor, client_id, new_balance)
        conn.commit()
        conn.close()
        return make_response(jsonify({"success": f"Your new balance is {new_balance}"}), 201)
    
@app.route('/withdraw', methods=["POST"])
def withdraw():
    conn, cursor = connect_db()
    if request.method == "POST":
        data = request.get_json()
        client_id = data['client_id']
        amount = float(data['quantity'])

        # Get client balance using helper function
        balance = get_client_balance(cursor, client_id)
        if balance is None:
            conn.close()
            return make_response(jsonify({"error": "Client not found"}), 404)

        new_balance = balance - amount
        if new_balance < 0:
            conn.close()
            return make_response(jsonify({"error": "Not enough funds to withdraw!(CONFLICT)"}), 409)

        # Update client balance using helper function
        update_client_balance(cursor, client_id, new_balance)
        conn.commit()
        conn.close()
        return make_response(jsonify({"success": f"Your new balance is {new_balance}"}), 201)
    

@app.route('/transactions/<string:start_end>', methods=["GET"])
def transactions(start_end = None):
    conn, cursor = connect_db()
    if request.method == "GET":
        start, end = start_end.split(";")[0], start_end.split(";")[1]
        transactions = get_transactions_between(cursor, start, end)
        conn.close()

        if transactions:
            data = []
            for t in transactions:
                data.append({
                    "time": t[0],
                    "asset_symbol": t[1],
                    "type": t[2],
                    "quantity": t[3],
                    "price": t[4]
                })
            return make_response(jsonify({"json": data}), 200)
        return make_response(jsonify({"error": "No transactions found"}), 404)


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 coincenter_flask.py server_ip server_port")
        sys.exit(1)
        
    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])
    
    if server_port <= 0:
        print("Error: The port number must be greater than 0")
        sys.exit(1)
        
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile='root.pem')
    context.load_cert_chain(certfile='serv.crt', keyfile='serv.key')
    app.run(debug=True, host=server_ip, port=server_port, ssl_context=context)

if __name__ == '__main__':
    main()
    # Finalizar o cliente Kazoo
    zh.stop()
    zh.close()