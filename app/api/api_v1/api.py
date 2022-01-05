from fastapi import APIRouter

from app.api.api_v1.endpoints import health, users

api_router = APIRouter()
api_router.include_router(health.router, prefix="/ping", tags=["ping"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
