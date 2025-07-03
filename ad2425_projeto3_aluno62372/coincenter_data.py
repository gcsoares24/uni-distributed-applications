"""
Aplicações Distribuídas - Projeto 2 - sock_utils.py
Números de aluno: 62372
"""

def add_client(cursor, balance, is_manager):
    cursor.execute(
            "INSERT INTO Clients (is_manager, balance) VALUES (?, ?)",
            (balance, is_manager))


def get_client(cursor, client_id):
    cursor.execute("SELECT * FROM Clients WHERE client_id = ?", (client_id,))
    client = cursor.fetchone()
    return client

def get_client_money(cursor, client_id):
    client = get_client(cursor, client_id)
    cursor.execute("SELECT asset_symbol, quantity FROM ClientAssets WHERE client_id = ?", (client_id,))
    clientAssets = cursor.fetchall()
    return client, clientAssets

def lastrowid(cursor):
    return cursor.lastrowid

def add_asset(cursor, symbol, name, price, available_supply):
    try:
        cursor.execute(
            "INSERT INTO Assets (asset_symbol, asset_name, price, available_quantity) VALUES (?, ?, ?, ?)",
            (symbol, name, price, available_supply)
        )
        return True, None
    except Exception as e:
        return False, str(e)

def get_asset(cursor, asset_symbol):
    cursor.execute(
        "SELECT asset_symbol, asset_name, price, available_quantity FROM Assets WHERE asset_symbol = ?",
        (asset_symbol,)
    )
    return cursor.fetchone()

def get_assets_by_symbols(cursor, asset_symbols):

    placeholders = ",".join("?" for _ in asset_symbols)
    query = f"SELECT asset_symbol, asset_name, price, available_quantity FROM Assets WHERE asset_symbol IN ({placeholders})"
    cursor.execute(query, asset_symbols)
    return cursor.fetchall()

def get_asset_price_and_quantity(cursor, symbol):
    cursor.execute("SELECT price, available_quantity FROM Assets WHERE asset_symbol = ?", (symbol,))
    return cursor.fetchone()

def get_client_balance(cursor, client_id):
    cursor.execute("SELECT balance FROM Clients WHERE client_id = ?", (client_id,))
    result = cursor.fetchone()
    return result[0] if result else None

def update_client_asset_quantity(cursor, client_id, symbol, new_quantity):
    cursor.execute(
        "UPDATE ClientAssets SET quantity = ? WHERE client_id = ? AND asset_symbol = ?",
        (new_quantity, client_id, symbol)
    )

def insert_client_asset(cursor, client_id, symbol, quantity):
    cursor.execute(
        "INSERT INTO ClientAssets (client_id, asset_symbol, quantity) VALUES (?, ?, ?)",
        (client_id, symbol, quantity)
    )
    
def process_transaction(cursor, client_id, new_balance, symbol, new_asset_quantity, tx_type, quantity, price, time):
    # Update client balance
    cursor.execute("UPDATE Clients SET balance = ? WHERE client_id = ?", (new_balance, client_id))
    # Update asset available quantity
    cursor.execute("UPDATE Assets SET available_quantity = ? WHERE asset_symbol = ?", (new_asset_quantity, symbol))
    # Insert transaction record
    cursor.execute(
        "INSERT INTO Transactions (client_id, asset_symbol, type, quantity, price, time) VALUES (?, ?, ?, ?, ?, ?)",
        (client_id, symbol, tx_type, quantity, price, time)
    )
    
def get_asset_price_and_available(cursor, symbol):
    cursor.execute("SELECT price, available_quantity FROM Assets WHERE asset_symbol = ?", (symbol,))
    return cursor.fetchone()

def get_client_asset_quantity(cursor, client_id, symbol):
    cursor.execute("SELECT quantity FROM ClientAssets WHERE client_id = ? AND asset_symbol = ?", (client_id, symbol))
    return cursor.fetchone()

def update_client_balance(cursor, client_id, balance):
    cursor.execute("UPDATE Clients SET balance = ? WHERE client_id = ?", (balance, client_id))
    
    
def get_transactions_between(cursor, start, end):
    cursor.execute(
        "SELECT time, asset_symbol, type, quantity, price FROM Transactions WHERE time > ? AND time < ?",
        (start, end)
    )
    return cursor.fetchall()