from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Product(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    descricao = Column(String, nullable=True)
    imagem_url = Column(String, nullable=True)

    pedidos = relationship("Order", back_populates="produto")


class Order(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)

    produto = relationship("Product", back_populates="pedidos")