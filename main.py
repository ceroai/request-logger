import json
import os

from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse

app = FastAPI()


@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    """
    Middleware to log incoming request details.
    """

    # Get the payload
    body = await request.body()
    payload = body.decode("utf-8")

    # Get the source IP
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
    return PlainTextResponse("", status_code=204)


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
