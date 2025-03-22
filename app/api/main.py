from fastapi import APIRouter

from app.api.routes import text


api_router = APIRouter()
api_router.include_router(text.router)

