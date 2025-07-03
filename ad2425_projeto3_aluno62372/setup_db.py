
import sqlite3
from os.path import isfile


# Função para conectar ao banco de dados SQLite
def connect_db():
    db_is_created = isfile('coincenter.db')
    connection = sqlite3.connect('coincenter.db')
    cursor = connection.cursor()
    if not db_is_created:
        # Create Clients table
        cursor.execute("""
            CREATE TABLE Clients (
                client_id INTEGER PRIMARY KEY AUTOINCREMENT,
                is_manager INTEGER NOT NULL DEFAULT 0,
                balance REAL DEFAULT 0
            );
        """)
        
        # Create Assets table
        cursor.execute("""
            CREATE TABLE Assets (
                asset_symbol TEXT PRIMARY KEY,
                asset_name TEXT NOT NULL,
                price REAL NOT NULL,
                available_quantity INTEGER NOT NULL
            );
        """)
        
        # Create ClientAssets table
        cursor.execute("""
            CREATE TABLE ClientAssets (
                client_id INTEGER NOT NULL,
                asset_symbol TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                PRIMARY KEY (client_id, asset_symbol),
                FOREIGN KEY (client_id) REFERENCES Clients(client_id),
                FOREIGN KEY (asset_symbol) REFERENCES Assets(asset_symbol)
                
            );
        """)
        
        # Create Transactions table
        cursor.execute("""
            CREATE TABLE Transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                client_id INTEGER NOT NULL,
                asset_symbol TEXT NOT NULL,
                type TEXT NOT NULL CHECK(type IN ('BUY', 'SELL')), -- BUY or SELL
                quantity INTEGER NOT NULL,
                price REAL NOT NULL,
                time DATETIME NOT NULL,
                FOREIGN KEY (client_id) REFERENCES Clients(client_id),
                FOREIGN KEY (asset_symbol) REFERENCES Assets(asset_symbol)
            );
        """)
        
        ##### INSERTS #####
        # 5 INSERTS FOR CRYPTO
        cursor.execute("""
            INSERT INTO Assets (asset_symbol, asset_name, price, available_quantity) VALUES
            ('BTC', 'Bitcoin', 65000, 100),
            ('ETH', 'Ethereum', 3500, 200),
            ('ADA', 'Cardano', 0.45, 10000),
            ('SOL', 'Solana', 150, 500),
            ('XRP', 'Ripple', 0.55, 8000);
        """)
        # MANAGER
        cursor.execute("""
            INSERT INTO Clients (client_id, is_manager, balance) VALUES (0, 1, 0);
        """)
        # USER FOR TESTING, HAS MONEY!
        cursor.execute("""
            INSERT INTO Clients (is_manager, balance) VALUES (0, 1000000);
        """)
        
        connection.commit()
    return connection, cursor



