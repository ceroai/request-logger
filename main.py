import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from schema import AgendamientoSchema
from pydantic import ValidationError
load_dotenv()

app = FastAPI()

PATH = "/agendamiento"

try: 
    VALID_TOKEN = os.getenv("AUTH_TOKEN")
except KeyError:
    print("⚠️ AUTH_TOKEN no encontrado en el archivo .env")
    VALID_TOKEN = None

def extract_token(request: Request) -> str | None:
    auth = request.headers.get("authorization", "")
    return auth.replace("Bearer ", "") if auth.startswith("Bearer ") else None

@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    """
    Middleware to log incoming request details.
    """

    if request.url.path != PATH:
        return JSONResponse(
            status_code=404,
            content={"message": "Not Valid Route", "path": request.url.path}
        )

    if request.method != "POST":
        return JSONResponse(status_code=405, content={"message": "Method not allowed"})

    token = extract_token(request)
    if not token:
        return JSONResponse(status_code=401, content={"message": "Missing Authorization header"})
    if token != VALID_TOKEN:
        return JSONResponse(status_code=401, content={"message": "Invalid token"})  


    body = await request.body()
    try:
        payload = AgendamientoSchema.model_validate_json(body)
    except ValidationError as e:
        return JSONResponse(status_code=400, content={"message": "Invalid payload", "error": str(e)})
    payload = body.decode("utf-8")

    source_ip = request.headers.get("X-Forwarded-For", request.client.host)

    # Prepare the log entry as a structured dictionary
    log_entry = {
        "message": "Incoming request",
        "url": str(request.url),
        "method": request.method,
        "source_ip": source_ip,
        "payload": payload,
        "headers": dict(request.headers),
    }

    # Print the log entry as a JSON string for structured logging in Cloud Run
    print(json.dumps(log_entry))

    response = await call_next(request)
    return response


@app.api_route(
    "/{path_name:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"]
)
async def catch_all(request: Request, path_name: str):
    """
    Catches all requests and returns a simple success message.
    """
    return JSONResponse(content={"success": True}, status_code=200)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
