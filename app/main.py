import os
import socket

from starlette.responses import JSONResponse
import uvicorn
from fastapi import FastAPI, Request

from app.config import PORT
from app.api.router import router as api_router
from app.shared.response import Error

app = FastAPI()

# Include master API router (/api)
app.include_router(api_router)


@app.get("/")
def view():
    return {
        "success": True,
        "message": "Hello, World!",
        "instance": {
            "pid": os.getpid(),
            "hostname": socket.gethostname(),
        },
    }


# Global 404 handler
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    error = Error(
        success=False,
        message="Route not found",
        details=f"Route '{request.url.path}' does not exist.",
    )

    return JSONResponse(
        status_code=404,
        content=error.model_dump(),
    )


# Global error handler
@app.exception_handler(Exception)
async def global_error_handler(request: Request, exc: Exception):
    error = Error(
        success=False,
        message="Internal server error",
        details=str(exc),
    )

    return JSONResponse(
        status_code=500,
        content=error.model_dump(),
    )


# ? Execution entrypoint when running: python main.py
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
