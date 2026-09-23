import time

from starlette.middleware.base import BaseHTTPMiddleware

from app.metrics import (
    ACTIVE_REQUESTS,
    REQUEST_COUNT,
    REQUEST_LATENCY,
)


class PrometheusMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        ACTIVE_REQUESTS.inc()
        start = time.time()

        try:
            response = await call_next(request)

            REQUEST_COUNT.labels(
                request.method,
                request.url.path,
                response.status_code,
            ).inc()

            return response

        finally:
            REQUEST_LATENCY.observe(time.time() - start)
            ACTIVE_REQUESTS.dec()
