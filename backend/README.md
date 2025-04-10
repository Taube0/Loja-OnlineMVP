# 🛠️ Loja Backend – FastAPI + PostgreSQL

API REST de pedidos e produtos para um sistema de loja online. Essa API permite listar produtos, registrar pedidos e popular os produtos a partir de uma API externa (FakeStore).

---

## 📦 Tecnologias

- Python 3.11
- FastAPI
- SQLAlchemy
- PostgreSQL
- Docker

---

## 🚀 Endpoints

| Método | Rota                | Descrição                          |
|--------|---------------------|------------------------------------|
| GET    | /produtos           | Lista todos os produtos            |
| POST   | /produtos           | Cria um novo produto               |
| POST   | /produtos/seed      | Importa produtos da FakeStore      |
| GET    | /pedidos            | Lista todos os pedidos             |
| POST   | /pedidos            | Cria um novo pedido                |
| PUT    | /pedidos/{id}       | Atualiza um pedido existente       |
| DELETE | /pedidos/{id}       | Remove um pedido existente         |

---

## 🧪 Instalação local (sem Docker)

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate.bat  # Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

---

## 🐳 Rodando com Docker

```bash
docker-compose build backend
docker-compose up backend
```

> Certifique-se de que o serviço `db` (PostgreSQL) também esteja definido no seu `docker-compose.yml`.

---

## 🔗 API Externa

Esta API consome dados da [FakeStore API](https://fakestoreapi.com/products) para popular os produtos automaticamente.

- 📌 Não exige autenticação  
- 🔓 Licença gratuita  
- 🔁 Uso: rota `/produtos/seed`

---

🔗 API Externa – Cálculo de Frete
Este projeto utiliza uma integração com a API de Cálculo de Frete dos Correios para estimar o valor do envio a partir de um CEP de origem fixo.

Origem: 55200-000 (Pesqueira – PE)

Destino: fornecido pelo usuário

Serviço: SEDEX (código 04014)

Peso e dimensões: simulados para uma caixa padrão de camiseta

Valor declarado: R$ 120,00

A API dos Correios não possui um endpoint oficial com autenticação gratuita para ambientes locais. Portanto, este MVP utiliza uma simulação controlada caso a chamada falhe.

✅ Documentação Técnica
Rota integrada: POST /frete

Parâmetro: cep_destino (string)

Resposta esperada:

{
  "valor": "24.90",
  "prazo": "3"
}

Observações:

Se a API oficial estiver offline ou bloqueada, retorna valor simulado

A simulação é claramente exibida no frontend

---

## 🗂️ Estrutura

```
backend/
├── frete.py          # Integração da API com um modelo de frete
├── main.py           # Entrada principal FastAPI
├── models.py         # Tabelas do banco (Produto, Pedido)
├── schemas.py        # Validação Pydantic
├── database.py       # Conexão com banco
├── Dockerfile        # Docker backend
├── requirements.txt
```

---

## 🖼️ Arquitetura

```
[ React Frontend ] → [ FastAPI Backend ] → [ PostgreSQL + FakeStoreAPI ]
```
