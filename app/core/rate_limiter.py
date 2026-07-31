from fastapi import Request
from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.core.config import settings


# Global limiter shared by the SlowAPIMiddleware (applies RATE_LIMIT_DEFAULT to
# every endpoint) and the per-route @limiter.limit(...) decorators (auth routes).
# Storage is in-memory: limits are per-process and reset on restart. Do not run
# multiple uvicorn workers with this setup (each worker enforces its own budget).
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.RATE_LIMIT_DEFAULT],
    headers_enabled=True,
    enabled=settings.RATE_LIMIT_ENABLED,
    strategy="fixed-window",
)


async def rate_limit_exceeded_handler(
    request: Request, exc: RateLimitExceeded
) -> JSONResponse:
    response = JSONResponse(
        status_code=429,
        content={"detail": "Too many requests. Please try again later."},
    )
    return request.app.state.limiter._inject_headers(
        response, request.state.view_rate_limit
    )
