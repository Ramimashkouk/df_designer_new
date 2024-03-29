from fastapi import APIRouter

from app.api.api_v1.endpoints import bot


api_router = APIRouter()
api_router.include_router(bot.router, prefix="/bot", tags=["bot"])
