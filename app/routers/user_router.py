from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.user_schema import User, UserResponse
from app.controllers.user_controller import create_user, get_all_users, get_user_by_nome, get_user_by_email, delete_user_by_id, login_user, get_current_user, update_user
from pydantic import BaseModel, EmailStr, Field

router = APIRouter(prefix="/users", tags=["users"])

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., description="E-mail do usuário")
    senha: str = Field(..., min_length=1, description="Senha do usuário")

class UpdateUserRequest(BaseModel):
    email: EmailStr = Field(..., description="Novo e-mail do usuário")
    senha: str = Field(..., min_length=1, description="Nova senha do usuário")

@router.post("/login", response_model=None)
async def login(login_data: LoginRequest):
    return await login_user(login_data.email, login_data.senha)

@router.post("/", status_code=201, response_model=UserResponse)
async def register_user(user: User):
    return await create_user(user)

@router.get("/", response_model=List[UserResponse])
async def get_users():
    return await get_all_users()

@router.get("/get/nome/{nome}", response_model=List[UserResponse])
async def get_users_by_nome(nome: str):
    return await get_user_by_nome(nome)

@router.get("/get/email/{email}", response_model=UserResponse)
async def get_user_by_email_route(email: str):
    return await get_user_by_email(email)

@router.delete("/{user_id}")
async def delete_user(user_id: str, user=Depends(get_current_user)):
    return await delete_user_by_id(user_id)

@router.put("/{user_id}", response_model=UserResponse)
async def update_user_route(user_id: str, update_data: UpdateUserRequest, user=Depends(get_current_user)):
    return await update_user(user_id, update_data.email, update_data.senha)
