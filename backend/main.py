from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import Base, Product, Order
from schemas import ProductCreate, ProductOut, OrderCreate, OrderOut
import requests
from frete import router as frete_router  # <-- adicionado

app = FastAPI()

# CORS para frontend React
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de dados
Base.metadata.create_all(bind=engine)

# Rota de frete
app.include_router(frete_router)  # <-- incluído

# ------------------ DB ------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ------------------ PRODUCTS ------------------

@app.get("/produtos", response_model=list[ProductOut])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/produtos", response_model=ProductOut)
def criar_produto(produto: ProductCreate, db: Session = Depends(get_db)):
    db_produto = Product(
        nome=produto.nome,
        preco=produto.preco,
        descricao=produto.descricao,
        imagem_url=produto.imagem_url
    )
    db.add(db_produto)
    db.commit()
    db.refresh(db_produto)
    return db_produto

@app.post("/produtos/seed", response_model=list[ProductOut])
def popular_produtos(db: Session = Depends(get_db)):
    try:
        response = requests.get("https://fakestoreapi.com/products")
        response.raise_for_status()
        dados = response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar dados externos: {e}")

    produtos_inseridos = []
    for item in dados:
        novo_produto = Product(
            nome=item["title"],
            preco=float(item["price"]),
            descricao=item.get("description", ""),
            imagem_url=item.get("image", "")
        )
        db.add(novo_produto)
        db.commit()
        db.refresh(novo_produto)
        produtos_inseridos.append(novo_produto)

    return produtos_inseridos

# ------------------ ORDERS ------------------

@app.get("/pedidos", response_model=list[OrderOut])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post("/pedidos", response_model=OrderOut)
def criar_pedido(pedido: OrderCreate, db: Session = Depends(get_db)):
    novo_pedido = Order(
        cliente=pedido.cliente,
        produto_id=pedido.produto_id
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

@app.put("/pedidos/{pedido_id}", response_model=OrderOut)
def atualizar_pedido(pedido_id: int, pedido: OrderCreate, db: Session = Depends(get_db)):
    db_pedido = db.query(Order).filter(Order.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db_pedido.cliente = pedido.cliente
    db_pedido.produto_id = pedido.produto_id
    db.commit()
    db.refresh(db_pedido)
    return db_pedido

@app.delete("/pedidos/{pedido_id}")
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = db.query(Order).filter(Order.id == pedido_id).first()
    if not db_pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(db_pedido)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}
