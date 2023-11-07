from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from prometheus_client import generate_latest

import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname).1s %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def read_user_by_id() -> Any:
    """
    Get metrics.
    """
    return generate_latest()

