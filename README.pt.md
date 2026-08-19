# CoinCenter: 3 Trabalhos de Sistemas Distribuídos

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Sockets](https://img.shields.io/badge/TCP%20Sockets-4B8BBE?style=for-the-badge&logo=cachet&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![SSL/TLS](https://img.shields.io/badge/TLS%2FSSL-721412?style=for-the-badge&logo=letsencrypt&logoColor=white)
![Apache ZooKeeper](https://img.shields.io/badge/Apache%20ZooKeeper-231F20?style=for-the-badge&logo=apache&logoColor=white)

> 📖 Quick note in English: This README is also available in English. To access it, just click [here](README.md).

## Sobre o projeto

Este repositório reúne três trabalhos práticos desenvolvidos para a unidade curricular de **Aplicações Distribuídas**, no ano letivo 24/25. Os três implementam o mesmo domínio — **CoinCenter**, um pequeno simulador de exchange de criptomoedas com um papel de gestor (que lista/adiciona/remove ativos) e papéis de utilizador (que depositam, levantam, compram e vendem) —, aprofundando progressivamente os conceitos de sistemas distribuídos: desde sockets em bruto, passando por uma separação estilo RPC (stub/skeleton) com I/O concorrente, até um serviço REST completo com persistência, TLS mútuo e coordenação distribuída.

### Funcionalidades

- **Projeto 1 — Sockets TCP em bruto**
  Implementa o cliente/servidor do CoinCenter diretamente sobre `socket` (`sock_utils.py`), com um protocolo de comunicação próprio prefixado por tamanho (`net_client.py` / `net_server.py`): um cabeçalho de 4 bytes com o tamanho, seguido de um payload serializado com `pickle`. A lógica de domínio (`coincenter_data.py`) modela clientes `Manager` e `User` que trocam comandos de texto separados por ponto e vírgula (`ADD_ASSET`, `BUY`, `SELL`, `DEPOSIT`, `WITHDRAW`, `GET_ASSETS_BALANCE`, ...).

- **Projeto 2 — Stub/skeleton (estilo RPC) + multiplexação de I/O**
  Refatora o mesmo domínio numa **stub** do lado do cliente (`coincenter_stub.py`), que transforma os comandos do menu em listas de pedidos com códigos numéricos, e numa **skeleton** do lado do servidor (`coincenter_skel.py`), que os despacha para o handler correspondente — a clássica separação, ao estilo RPC/RMI, entre a interface de chamada e a implementação remota. O servidor (`coincenter_server.py`) deixa também de suportar apenas uma ligação bloqueante de cada vez, passando a usar multiplexação de I/O com `select()`, servindo vários clientes em simultâneo numa única thread.

- **Projeto 3 — API REST, SQLite, TLS mútuo e ZooKeeper**
  Reimplementa o CoinCenter como uma API REST em HTTPS com **Flask** (`coincenter_flask.py`), persistindo clientes, ativos, posições e um registo de transações numa base de dados **SQLite** (`setup_db.py`, `bd.sql`). O canal é protegido com **TLS mútuo**: uma CA raiz autoassinada emite tanto o certificado do servidor (`serv.crt`/`serv.key`) como o certificado do cliente (`cli.crt`/`cli.key`), e o servidor Flask exige e valida o certificado do cliente (`ssl.CERT_REQUIRED`). Integra ainda o **Apache ZooKeeper** através do cliente `kazoo`: novos ativos são publicados como znodes efémeros sob `/assets`, e os clientes utilizadores ligados registam um `ChildrenWatch` para receberem notificações em tempo real sempre que o gestor adiciona um novo ativo.

### Stack tecnológica

- Python 3
- Sockets TCP em bruto (`socket`) com protocolo de comunicação próprio, prefixado por tamanho e baseado em `pickle`
- Arquitetura cliente/servidor stub-skeleton (estilo RPC/RMI)
- Multiplexação de I/O com `select()`
- Flask (API REST/HTTPS)
- SQLite (`sqlite3`)
- Autenticação TLS mútua com certificados autoassinados (módulo `ssl` do Python)
- Apache ZooKeeper através do cliente `kazoo` (coordenação distribuída, nós efémeros, watches)
- `requests` (biblioteca cliente HTTP)
