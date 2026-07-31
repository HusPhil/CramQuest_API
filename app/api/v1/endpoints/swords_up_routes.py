from typing import Optional

from fastapi import APIRouter, Header, Query, Request
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.rate_limiter import limiter

router = APIRouter()


@router.get("")
@limiter.limit(settings.SWORDS_UP_RATE_LIMIT)
async def swords_up(
    request: Request,
    api_key: Optional[str] = Query(default=None),
    x_api_key: Optional[str] = Header(default=None, alias="x-heartbeat-key"),
) -> JSONResponse:
    if not settings.SWORDS_UP_API_KEY:
        return JSONResponse(
            status_code=503,
            content={"detail": "Heartbeat endpoint is not configured"},
        )

    provided_key = api_key or x_api_key
    if not provided_key:
        return JSONResponse(status_code=401, content={"detail": "Missing API key"})

    if provided_key != settings.SWORDS_UP_API_KEY:
        return JSONResponse(status_code=403, content={"detail": "Invalid API key"})

    return JSONResponse(content={"status": "ok", "message": "Swords up!"})
