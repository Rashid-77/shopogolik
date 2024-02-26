from typing import Any

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def ping() -> Any:
    """Liveness probe"""
    return {"status": "ok"}
