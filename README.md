# 🧩 Loja Online – Projeto Full Stack com Docker

Sistema completo de loja online com frontend em React, backend em FastAPI e banco de dados PostgreSQL. Cada componente roda em seu próprio container com Docker, seguindo a arquitetura de microsserviços simples.

---

## 📦 Componentes

| Serviço   | Tecnologias                    | Descrição                              |
|-----------|--------------------------------|----------------------------------------|
| frontend  | React, Axios                   | Interface de compra e visualização     |
| backend   | FastAPI, SQLAlchemy, PostgreSQL| API REST para produtos e pedidos       |
| db        | PostgreSQL                     | Banco de dados relacional              |
| externo   | [FakeStore API](https://fakestoreapi.com) | Fonte dos produtos simulados  |

---

## 🚀 Como rodar tudo com Docker

Na raiz do projeto (onde está o `docker-compose.yml`), execute:

```bash
docker-compose up --build
```

Após a inicialização:

- 🖥️ Acesse o **frontend** em: [http://localhost:3000](http://localhost:3000)
- ⚙️ Acesse a **API (FastAPI)** em: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 📁 Estrutura do Projeto

```
.
├── backend/           # API FastAPI
│   └── README.md
├── frontend/          # Interface React
│   └── README.md
├── docker-compose.yml
└── README.md          # Este arquivo
```

---

## 🖼️ Arquitetura

```
[ React Frontend ] → [ FastAPI Backend ] → [ PostgreSQL ]
                               ↑
                         [ FakeStore API ]
```

---

## 📚 Mais informações

- 📄 [`frontend/README.md`](./frontend/README.md)
- 📄 [`backend/README.md`](./backend/README.md)
