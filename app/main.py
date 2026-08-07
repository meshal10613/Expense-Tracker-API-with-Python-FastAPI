import uvicorn
from fastapi import FastAPI

from app.config import PORT
from app.api.router import router as api_router
from app.shared.sendResponse import StandardResponse

app = FastAPI()

# Include master API router (/api)
app.include_router(api_router)

@app.get("/", response_model=StandardResponse[str], response_model_exclude_none=True)
def view():
    return StandardResponse(
        success=True,
        message="Hello, World!",
    )

#? Execution entrypoint when running: python main.py
if __name__ == "__main__":
    #* Run uvicorn server programmatically using PORT from config
    uvicorn.run("main:app", host="0.0.0.0", port=PORT, reload=True)