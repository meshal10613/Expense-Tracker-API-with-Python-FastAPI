import os
import socket

import uvicorn
from fastapi import FastAPI

from app.config import PORT
from app.api.router import router as api_router

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


# ? Execution entrypoint when running: python main.py
if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=PORT,
        proxy_headers=True,
        forwarded_allow_ips="*",
    )
