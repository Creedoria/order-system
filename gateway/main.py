from fastapi import FastAPI, Request
import httpx

app = FastAPI()

services = {
    "/api/v1/users": "http://localhost:8080",
    "/api/v1/items": "http://localhost:8001",
    "/api/v1/search": "http://localhost:8001",
    "/api/v1/cart": "http://localhost:8001",
    "/api/v1/orders": "http://localhost:8001"
}


@app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def gateway(full_path: str, request: Request):

    path = "/" + full_path

    target_service = None

    # Find matching service prefix
    for prefix, url in services.items():
        if path.startswith(prefix):
            target_service = url
            break

    if not target_service:
        return {"error": "Service not found"}

    target_url = f"{target_service}{path}"

    async with httpx.AsyncClient() as client:
        response = await client.request(
            method=request.method,
            url=target_url,
            content=await request.body(),
            headers=dict(request.headers)
        )

    return response.json()