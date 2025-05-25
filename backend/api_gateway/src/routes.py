# backend/api_gateway/src/routes.py
import logging
from fastapi import APIRouter, Request
from fastapi.responses import Response
import httpx
from config.api_gateway_settings import APIGatewaySettings

# Load from local .env
settings = APIGatewaySettings()

router = APIRouter()



@router.get("/frontend-config")
def get_config():
    logging.info("📦 /frontend-config HIT")

    return {
        "API_BASE_URL": settings.API_BASE_URL,
        "COVER_LETTER_SERVICE_URL": settings.COVER_LETTER_SERVICE_URL
    }

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_cover_letter(path: str, request: Request) -> Response:
    """
    Proxies incoming API requests to the cover letter service.

    Args:
        path (str): Path after the root to proxy (e.g. /files/upload)
        request (Request): Incoming request

    Returns:
        Response: Forwarded response from microservice
    """

    # 🚫 Prevent accidental routing loop for /frontend-config
    if path == "frontend-config":
        return Response(
            content='{"error":"Misrouted: /frontend-config is not a proxy route"}',
            media_type="application/json",
            status_code=400
        )

    # Define internal service address and target URL
    INTERNAL_COVER_LETTER_SERVICE_URL = "http://service_cover_letter:8010"
    target_url = f"{INTERNAL_COVER_LETTER_SERVICE_URL}/{path}"

    # ✅ Now it's safe to log
    logging.info(f"🔁🔁 Proxy target_url: {target_url}")

    query_params = request.query_params
    body = await request.body()

    

    async with httpx.AsyncClient() as client:
        forward_response = await client.request(
            method=request.method,
            url=target_url,
            headers=dict(request.headers),
            params=query_params,
            content=body,
            follow_redirects=False,
            timeout=15.0,
        )

    logging.info(f"🔁 Proxying {request.method} to: {target_url}")
    logging.info(f"🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁🔁  {request.method} {path} → {target_url}")

    return Response(
        content=forward_response.content,
        status_code=forward_response.status_code,
        media_type=forward_response.headers.get("Content-Type"),
    )
