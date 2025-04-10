from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from database import get_db
from models import Pedido
from schemas import PedidoCreate, PedidoResponse

router = APIRouter()

FAKESTORE_API = "https://fakestoreapi.com/products"

@router.get("/produtos", tags=["Produtos"], summary="Lista produtos da FakeStore API")
def listar_produtos():
    response = requests.get(FAKESTORE_API)
    return response.json()

@router.post("/pedidos", response_model=PedidoResponse, tags=["Pedidos"], summary="Cria um novo pedido")
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = Pedido(
        nome_cliente=pedido.nome_cliente,
        produto=pedido.produto,
        preco=pedido.preco,
        quantidade=pedido.quantidade
    )
    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido

@router.get("/pedidos", response_model=list[PedidoResponse], tags=["Pedidos"], summary="Lista todos os pedidos")
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

@router.put("/pedidos/{pedido_id}", tags=["Pedidos"], summary="Atualiza um pedido pelo ID")
def atualizar_pedido(pedido_id: int, status: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    pedido.status = status
    db.commit()
    return pedido

@router.delete("/pedidos/{pedido_id}", tags=["Pedidos"], summary="Deleta um pedido pelo ID")
def deletar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    db.delete(pedido)
    db.commit()
    return {"message": "Pedido deletado com sucesso"}