from fastapi import APIRouter
from starlette import status
from app.shared.response import Success

router = APIRouter(prefix="/v1", tags=["v1"])


@router.get(
    "/",
    response_model=Success[dict],
    status_code=status.HTTP_200_OK,
)
def health_check():
    return Success(success=True, message="API is healthy", data={"status": "healthy"})
