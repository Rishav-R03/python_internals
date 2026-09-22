# Custom middleware to record:
    # - total HTTP requests (by method, endpoint, status)

import time 
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response 

from .metrics import REQUEST_COUNT,REQUEST_LATENCY

class PrometheusMiddleware(BaseHTTPMiddleware):
    """Times  each request and updates Prometheus metrics"""
    async def dispatch(self,request: Request,call_next) -> Response:
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start_time

        route = request.scope.get("route")
        endpoint = route.path if route else request.url.path 

        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=endpoint,
            status_code=response.status_code
        ).inc()

        REQUEST_LATENCY.labels(
            method=request.method,
            endpoint=endpoint,
        ).observe(duration)

        return response 

