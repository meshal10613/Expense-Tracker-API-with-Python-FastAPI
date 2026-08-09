from fastapi import APIRouter
from starlette import status
from app.shared.response import Success
from app.api.v1.expenses.router import router as expenses_router

router = APIRouter(prefix="/v1", tags=["v1"])


router.include_router(expenses_router)
