from typing import Optional

class UserModel:
    def __init__(self, nome: str, email: str, senha: str, id: Optional[str] = None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha

    def to_dict(self):
        data = {
            "nome": self.nome,
            "email": self.email,
            "senha": self.senha
        }
        if self.id is not None:
            data["_id"] = self.id
        return data

    @staticmethod
    def from_dict(data: dict):
        return UserModel(
            id=str(data.get("_id")),
            nome=data.get("nome"),
            email=data.get("email"),
            senha=data.get("senha")
        )
