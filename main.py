from fastapi import FastAPI
from app.routers import user_router
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi import status, Request

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "erro": "Erro de validação nos dados enviados.",
            "detalhes": exc.errors(),
            "body": exc.body
        },
    )

app.include_router(user_router.router)
