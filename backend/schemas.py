from pydantic import BaseModel, EmailStr

class ProductCreate(BaseModel):
    nome: str
    preco: float
    descricao: str
    imagem_url: str

class ProductOut(ProductCreate):
    id: int
    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    cliente: str
    produto_id: int

class OrderOut(OrderCreate):
    id: int
    class Config:
        from_attributes = True

# -------- AUTH --------
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str
