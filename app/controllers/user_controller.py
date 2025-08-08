from fastapi import HTTPException, Depends
from app.models.user_model import UserModel
from app.schemas.user_schema import User, UserResponse
from app.database import mongodb
from passlib.context import CryptContext
from typing import List
from bson import ObjectId
from jose import jwt
import os
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

async def create_user(user: User) -> UserResponse:
    existing_user = await mongodb.user_collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado.")
    hashed_password = hash_password(user.senha)
    user_model = UserModel(nome=user.nome, email=user.email, senha=hashed_password)
    result = await mongodb.user_collection.insert_one(user_model.to_dict())
    user_model.id = str(result.inserted_id)
    return UserResponse(id=user_model.id, nome=user_model.nome, email=user_model.email)

async def get_all_users() -> List[UserResponse]:
    users_cursor = mongodb.user_collection.find()
    users = []
    async for user in users_cursor:
        users.append(UserResponse(
            id=str(user["_id"]),
            nome=user["nome"],
            email=user["email"]
        ))
    return users

async def get_user_by_nome(nome: str) -> List[UserResponse]:
    users_cursor = mongodb.user_collection.find({"nome": nome})
    users = []
    async for user in users_cursor:
        users.append(UserResponse(
            id=str(user["_id"]),
            nome=user["nome"],
            email=user["email"]
        ))
    return users

async def get_user_by_email(email: str) -> UserResponse:
    user = await mongodb.user_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return UserResponse(
        id=str(user["_id"]),
        nome=user["nome"],
        email=user["email"]
    )

async def delete_user_by_id(user_id: str):
    try:
        object_id = ObjectId(user_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido.")
    result = await mongodb.user_collection.delete_one({"_id": object_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return {"detail": "Usuário deletado com sucesso."}

async def login_user(email: str, senha: str):
    user = await mongodb.user_collection.find_one({"email": email})
    if not user or not pwd_context.verify(senha, user["senha"]):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")
    token_data = {"user_id": str(user["_id"]), "email": user["email"]}
    token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
    return {"user": UserResponse(id=str(user["_id"]), nome=user["nome"], email=user["email"]), "access_token": token}

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Token não fornecido.")
    return verify_token(credentials.credentials)

async def update_user(user_id: str, new_email: str, new_password: str) -> UserResponse:
    existing_user = await mongodb.user_collection.find_one({"email": new_email, "_id": {"$ne": ObjectId(user_id)}})
    if existing_user:
        raise HTTPException(status_code=400, detail="E-mail já cadastrado por outro usuário.")
    hashed_password = hash_password(new_password)
    result = await mongodb.user_collection.find_one_and_update(
        {"_id": ObjectId(user_id)},
        {"$set": {"email": new_email, "senha": hashed_password}},
        return_document=True
    )
    if not result:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")
    return UserResponse(id=str(result["_id"]), nome=result["nome"], email=result["email"])
