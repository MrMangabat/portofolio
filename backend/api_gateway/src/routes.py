#backend/api_gateway/src/routes.py

import logging
from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
import httpx
from config.dependencies import get_api_gateway_settings
from config.config_combined_settings import CombinedSettings

router = APIRouter()


@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_cover_letter(
    path: str,
    request: Request,
    settings: CombinedSettings = Depends(get_api_gateway_settings)
):
    service_url = settings.top.COVER_LETTER_SERVICE_URL
    async with httpx.AsyncClient() as client:
        url = f"{service_url}/{path}"
        params = request.query_params
        body = await request.body()
        # Use allow_redirects=False in case of status code 307/308
        forward_response = await client.request(request.method, url, headers=dict(request.headers), params=params, content=body, follow_redirects=False)
        
        # Build a FastAPI Response, letting CORS middleware add headers
        return Response(
            content=forward_response.content,
            status_code=forward_response.status_code,
            media_type=forward_response.headers.get("Content-Type")
        )
    

@router.get("/frontend-config")
def get_config(settings: CombinedSettings = Depends(get_api_gateway_settings)):
    """Return dynamic environment settings for the frontend."""
    return {
        "API_BASE_URL": settings.top.API_BASE_URL,
        "COVER_LETTER_SERVICE_URL": f"{settings.top.COVER_LETTER_SERVICE_URL}/cover-letter"
    }