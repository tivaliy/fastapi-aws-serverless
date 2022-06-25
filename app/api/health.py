from typing import Dict

from fastapi import APIRouter

health_router = APIRouter()


@health_router.get("", response_model=Dict[str, str])
async def ping() -> Dict[str, str]:
    """
    Health Check.
    """
    return {"ping": "pong"}
