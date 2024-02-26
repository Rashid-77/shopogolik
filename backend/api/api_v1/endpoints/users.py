from fastapi import APIRouter
from prometheus_client import Histogram

router = APIRouter()

REQUEST_TIME_BACKET = Histogram(
    "request_latency_seconds", "Time spent processing request", ["endpoint"]
)
