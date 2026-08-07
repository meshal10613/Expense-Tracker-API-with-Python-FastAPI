from typing import List
from fastapi import APIRouter
from app.shared.sendResponse import StandardResponse, Meta

router = APIRouter(prefix="/v1", tags=["v1"])

@router.get("/items", response_model=StandardResponse[List[str]])
def get_items():
    return StandardResponse(
        success=True,
        message="Items retrieved successfully",
        data=["item1", "item2", "item3"],
        meta=Meta(
            page=1,
            limit=10,
            total=3,
            total_pages=1
        )
    )
