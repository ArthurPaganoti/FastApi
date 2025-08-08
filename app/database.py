from motor.motor_asyncio import AsyncIOMotorClient
import logging

MONGO_DETAILS = "mongodb://localhost:27017"

logging.basicConfig(level=logging.INFO)


class DataBase:
    def __init__(self):
        try:
            self.client = AsyncIOMotorClient(MONGO_DETAILS)
            self.db = self.client["fastapi_db"]
            self.user_collection = self.db["user"]
            logging.info("Conexão com MongoDB estabelecida com sucesso.")
        except Exception as e:
            logging.error(f"Erro ao conectar ao MongoDB: {e}")


mongodb = DataBase()
