import time
from fastapi import FastAPI
from fastapi import Request
from prometheus_client import Counter, Histogram, Info

from api.api_v1.api import api_router

from utils import get_settings

import logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname).1s %(message)s",
    datefmt="%Y.%m.%d %H:%M:%S",
)
    
logger = logging.getLogger(__name__)
app = FastAPI()
app.include_router(api_router, prefix=get_settings().API_V1_STR)


METRICS_REQUEST_LATENCY = Histogram(
    "app_request_latency_seconds", 
    "Application Request Latency", 
    ["method", "endpoint"]
)

METRICS_REQUEST_COUNT = Counter(
    "app_request_count",
    "Application Request Count",
    ["method", "endpoint", "http_status"],
)

METRICS_INFO = Info("app_version", "Application Version")


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    before_request(request)

    response = await call_next(request)
    
    after_request(request, response)
    return response


def before_request(request: Request):
    request._prometheus_metrics_request_start_time = time.time()


def after_request(request: Request, response):
    url = str(request.url)
    if 'metrics' in url:
        return response

    request_latency = time.time() - request._prometheus_metrics_request_start_time
    if 'user' in url:
        url = '/'.join(url.split('/')[:-1]) + '/'
    logger.info(url)
    METRICS_REQUEST_LATENCY.labels(request.method, url).observe(
        request_latency
    )
    METRICS_REQUEST_COUNT.labels(
        request.method, url, response.status_code
    ).inc()
    return response


def register_metrics(app_version=None, app_config=None):
    METRICS_INFO.info({"version": "1", "config": "develop"})


register_metrics()
