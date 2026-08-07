from fastapi import APIRouter
from app.api.v1.router import router as v1_router

router = APIRouter(prefix="/api")

# Aggregate sub-routers
router.include_router(v1_router)
