# Distributed Applications Projects

This repository contains three projects related to distributed applications, developed for the AD2425 course. Each project demonstrates different aspects of distributed systems, networking, and security.

## Projects Overview

### 1. Projeto 1
- **Folder:** `ad2425_projeto1_aluno-62372/`
- **Description:**
  - Implements basic client-server communication using sockets.
  - Files include: `coincenter_client.py`, `coincenter_server.py`, `net_client.py`, `net_server.py`, `sock_utils.py`, and `coincenter_data.py`.

### 2. Projeto 2
- **Folder:** `ad2425_projeto2_aluno-62372/`
- **Description:**
  - Extends the first project with stubs and skeletons for remote method invocation.
  - Adds files: `coincenter_skel.py`, `coincenter_stub.py`.
  - Continues to use and improve upon the networking and data handling modules.

### 3. Projeto 3
- **Folder:** `ad2425_projeto3_aluno62372/`
- **Description:**
  - Introduces database integration and security with SSL/TLS.
  - Includes a Flask-based server (`coincenter_flask.py`), database setup scripts, and certificate/key files for secure communication.
  - Files include: `setup_db.py`, `bd.sql`, `coincenter_utils.py`, and various certificate/key files.

## Getting Started

### Requirements
- Python 3.x
- Flask (for Project 3)
- SQLite (for Project 3)

### Running the Projects

#### Project 1 & 2
1. Navigate to the respective project folder.
2. Run the server:
   ```bash
   python3 coincenter_server.py
   ```
3. In another terminal, run the client:
   ```bash
   python3 coincenter_client.py
   ```

#### Project 3
1. Navigate to `ad2425_projeto3_aluno62372/`.
2. Set up the database:
   ```bash
   python3 setup_db.py
   ```
3. Start the Flask server (with SSL):
   ```bash
   python3 coincenter_flask.py
   ```
4. Run the client:
   ```bash
   python3 coincenter_client.py
   ```

## Security
- Project 3 uses SSL/TLS certificates for secure communication.
- Certificate and key files are included for demonstration purposes.

## License
This repository is for educational purposes.
