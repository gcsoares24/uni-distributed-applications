# CoinCenter: 3 Distributed Systems Labs

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Sockets](https://img.shields.io/badge/TCP%20Sockets-4B8BBE?style=for-the-badge&logo=cachet&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![SSL/TLS](https://img.shields.io/badge/TLS%2FSSL-721412?style=for-the-badge&logo=letsencrypt&logoColor=white)
![Apache ZooKeeper](https://img.shields.io/badge/Apache%20ZooKeeper-231F20?style=for-the-badge&logo=apache&logoColor=white)

> 📖 Quick note in Portuguese: You can also read this README in Portuguese. To do so, just access [here](README.pt.md).

## About the project

This repository holds three incremental lab projects built for the **Distributed Applications** (*Aplicações Distribuídas*) course, academic year 24/25. All three implement the same domain — **CoinCenter**, a small cryptocurrency exchange simulator with a manager role (who lists/adds/removes assets) and user roles (who deposit, withdraw, buy and sell) — while progressively layering on more distributed-systems concepts: from raw sockets, to an RPC-style stub/skeleton split with concurrent I/O, to a full REST service with persistence, mutual TLS and distributed coordination.

### Features

- **Projeto 1 — Raw TCP sockets**
  Implements the CoinCenter client/server directly over `socket` (`sock_utils.py`), with a custom length-prefixed wire protocol (`net_client.py` / `net_server.py`): a 4-byte size header followed by a `pickle`-serialized payload. The domain logic (`coincenter_data.py`) models `Manager` and `User` clients that exchange semicolon-delimited text commands (`ADD_ASSET`, `BUY`, `SELL`, `DEPOSIT`, `WITHDRAW`, `GET_ASSETS_BALANCE`, ...).

- **Projeto 2 — Stub/skeleton (RPC-style) + I/O multiplexing**
  Refactors the same domain into a client-side **stub** (`coincenter_stub.py`) that turns menu commands into numeric-coded request lists, and a server-side **skeleton** (`coincenter_skel.py`) that dispatches them to the matching handler — a classic RPC/RMI-style separation between the calling interface and the remote implementation. The server (`coincenter_server.py`) also moves from one blocking connection to `select()`-based I/O multiplexing, so it can serve several clients concurrently on a single thread.

- **Projeto 3 — REST API, SQLite, mutual TLS and ZooKeeper**
  Reimplements CoinCenter as an HTTPS REST API with **Flask** (`coincenter_flask.py`), persisting clients, assets, holdings and a transaction log in a **SQLite** database (`setup_db.py`, `bd.sql`). The channel is secured with **mutual TLS**: a self-signed root CA issues both the server certificate (`serv.crt`/`serv.key`) and the client certificate (`cli.crt`/`cli.key`), and the Flask server requires and verifies the client cert (`ssl.CERT_REQUIRED`). It also integrates **Apache ZooKeeper** through the `kazoo` client: new assets are published as ephemeral znodes under `/assets`, and connected user clients register a `ChildrenWatch` to get live notifications when the manager adds a new asset.

### Tech stack

- Python 3
- Raw TCP sockets (`socket`) with a custom length-prefixed, `pickle`-based framing protocol
- Client/server stub-skeleton (RPC/RMI-style) architecture
- I/O multiplexing with `select()`
- Flask (REST/HTTPS API)
- SQLite (`sqlite3`)
- Mutual TLS authentication with self-signed certificates (Python `ssl` module)
- Apache ZooKeeper via the `kazoo` client (distributed coordination, ephemeral nodes, watches)
- `requests` (HTTP client library)
