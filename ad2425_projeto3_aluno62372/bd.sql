"""
Aplicações Distribuídas - Projeto 3 - bd.sql
Número do aluno: 62372
"""

-- Tabela Clients
CREATE TABLE Clients (
    client_id INTEGER PRIMARY KEY AUTOINCREMENT,
    is_manager INTEGER NOT NULL DEFAULT 0,
    balance REAL DEFAULT 0
);

-- Tabela Assets
CREATE TABLE Assets (
    asset_symbol TEXT PRIMARY KEY,
    asset_name TEXT NOT NULL,
    price REAL NOT NULL,
    available_quantity INTEGER NOT NULL
);

-- Tabela ClientAssets
CREATE TABLE ClientAssets (
    client_id INTEGER NOT NULL,
    asset_symbol TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    PRIMARY KEY (client_id, asset_symbol),
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (asset_symbol) REFERENCES Assets(asset_symbol)
);

-- Tabela Transactions
CREATE TABLE Transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id INTEGER NOT NULL,
    asset_symbol TEXT NOT NULL,
    type TEXT NOT NULL CHECK(type IN ('BUY', 'SELL')), -- BUY ou SELL
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,
    time DATETIME NOT NULL,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (asset_symbol) REFERENCES Assets(asset_symbol)
);
