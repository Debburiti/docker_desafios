# 🐳 Repositório: docker_desafios

---

## 🛠️ Pré-requisitos

Para executar os desafios, você deve ter instalados:

* **Docker Engine:** Versão 20.10.0 ou superior.
* **Docker Compose:** Versão v2.0.0 ou superior.
* **Git:** Para clonar o repositório.

## 🚀 Como Executar o Projeto

1.  **Clonar o Repositório:**
    ```bash
    git clone [LINK DO SEU REPOSITÓRIO]
    cd nome-do-seu-projeto
    ```

2.  **Configurar Variáveis de Ambiente (Desafios 2 e 3):**
    Crie o arquivo `.env` nas pastas `desafio2/` e `desafio3/` para que os serviços de banco de dados iniciem corretamente.

    * **Importante:** O arquivo `.env` é **ignorado** pelo `.gitignore` por razões de segurança, mas é necessário para a execução local.

3.  **Executar Individualmente:** Navegue até a pasta do desafio desejado (`cd desafioX/`) e utilize o comando `docker compose up -d`.

---

## 1. Desafio 1 — Containers em Rede

### 💻 Solução e Arquitetura

Este desafio demonstra o **DNS interno** provido por uma rede customizada do Docker.

* **Rede:** `desafio-1` (Driver `bridge`).
* **Serviço 1 (Servidor):** `servidor-web` (Imagem Nginx, porta 80 interna).
* **Serviço 2 (Cliente):** `cliente-curl` (Imagem Alpine), que executa um *script* `curl` em *loop* apontando para o hostname `servidor-web`.

A comunicação é feita diretamente pelo nome do serviço, provando que a rede customizada está funcional.

### 🧪 Instruções de Teste

1.  Suba os serviços:
    ```bash
    cd desafio1
    docker compose up -d
    ```
2.  Visualize os logs do Nginx, que registrarão as requisições periódicas do `cliente-curl`:
    ```bash
    docker logs servidor-web -f
    ```

---

## 2. Desafio 2 — Volumes e Persistência

### 💻 Solução e Arquitetura

A persistência de dados é garantida pelo uso de um **Volume Nomeado** do Docker, a abordagem recomendada para dados de produção.

* **Serviço:** `postgres-db` (PostgreSQL).
* **Persistência:** O volume `desafio2_pgdata` é mapeado para o diretório de dados padrão do PostgreSQL: `/var/lib/postgresql/data`.
* **Segurança:** As credenciais de acesso são fornecidas pelo arquivo **`.env`** local, seguindo as boas práticas para o Git.

### 🧪 Instruções de Teste

1.  Suba o serviço (Certifique-se que o `.env` esteja criado):
    ```bash
    cd desafio2
    docker compose up -d
    ```
2.  **Passo A: Inserção de Dados (Escrita)**
    * Acesse o terminal do banco: `docker exec -it postgres-db psql -U usuario`
    * Crie e insira dados: `CREATE TABLE teste (id INT); INSERT INTO teste (id) VALUES (42); \q`
3.  **Passo B: Recriação do Container (Teste de Persistência)**
    * Remova o container (MANTENDO O VOLUME): `docker compose stop && docker compose rm -f`
    * Suba um NOVO container: `docker compose up -d`
4.  **Passo C: Verificação**
    * Acesse o novo container: `docker exec -it postgres-db psql -U usuario`
    * Verifique os dados: `SELECT * FROM teste;` -> O valor `42` deve persistir.
5.  Limpeza Total (Remove Container e Volume): `docker compose down -v`

---

## 3. Desafio 3 — Docker Compose Orquestrando Serviços

### 💻 Solução e Arquitetura

O `docker-compose.yml` orquestra uma arquitetura de 3 camadas, utilizando a rede interna `desafio3_rede`.

* **Serviços:** `db` (PostgreSQL), `cache` (Redis) e `web` (Nginx).
* **Dependência:** O serviço `web` utiliza `depends_on: [db, cache]` para garantir que os serviços de apoio sejam iniciados antes da aplicação principal.
* **Comunicação:** Todos os serviços se comunicam usando seus nomes (ex: `db` e `cache`) na rede.

### 🧪 Instruções de Teste

1.  Suba os serviços (Certifique-se que o `.env` esteja criado):
    ```bash
    cd desafio3
    docker compose up -d
    ```
2.  **Teste de Comunicação (DNS):**
    * Execute um container Alpine temporário na mesma rede para pingar os serviços:
        ```bash
        docker run --rm --network desafio3_rede alpine ping -c 3 db
        docker run --rm --network desafio3_rede alpine ping -c 3 cache
        ```
    * Ambos os comandos devem retornar sucesso, provando que a orquestração de rede e DNS funcionou.

---

## 4. Desafio 4 — Microsserviços Independentes

### 💻 Solução e Arquitetura

Implementação de dois microsserviços **Flask** com seus respectivos `Dockerfile`s e comunicação direta via HTTP.

* **Serviço A (`data-service`):** Fornece dados JSON na porta 5000.
    * **Dockerfile:** Instala Flask e expõe `app.py`.
* **Serviço B (`consumer-api`):** Microsserviço consumidor (porta 5001).
    * **Comunicação:** Usa a biblioteca `requests` para fazer `GET http://data-service:5000/usuarios`.
    * **Dockerfile:** Instala Flask e a biblioteca `requests`.

### 🧪 Instruções de Teste

1.  Suba os serviços (o `--build` é necessário para compilar as imagens Flask):
    ```bash
    cd desafio4
    docker compose up --build -d
    ```
2.  **Teste do Consumidor:** Acesse a API do serviço B, que deve retornar o HTML formatado com dados puxados do serviço A:
    ```bash
    curl http://localhost:5001/
    ```

---

## 5. Desafio 5 — Microsserviços com API Gateway

### 💻 Solução e Arquitetura

Implementação de um padrão **API Gateway** usando **Nginx** como *Proxy Reverso* para centralizar o acesso a dois microsserviços internos (Flask).

* **Gateway:** `api-gateway` (Nginx). O arquivo `gateway-nginx/nginx.conf` é montado via volume e define as regras de roteamento.
* **Serviço 1:** `user-service` (Flask, porta 5000 interna).
* **Serviço 2:** `order-service` (Flask, porta 5000 interna).
* **Roteamento (Nginx):**
    * `/users` -> Proxy para `http://user-service:5000`
    * `/orders` -> Proxy para `http://order-service:5000`

### 🧪 Instruções de Teste

1.  Suba os serviços:
    ```bash
    cd desafio5
    docker compose up -d
    ```
2.  **Teste Rota de Usuários (via Gateway):**
    ```bash
    curl http://localhost/users
    ```
    * O Gateway roteia a chamada para o `user-service`.
3.  **Teste Rota de Pedidos (via Gateway):**
    ```bash
    curl http://localhost/orders
    ```
    * O Gateway roteia a chamada para o `order-service`.

---
