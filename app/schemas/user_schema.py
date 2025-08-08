from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class User(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome do usuário")
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")

class UserResponse(BaseModel):
    id: str
    nome: str
    email: EmailStr

    class Config:
        orm_mode = True
