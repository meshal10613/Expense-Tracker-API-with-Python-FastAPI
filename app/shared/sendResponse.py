from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar("T")

class Meta(BaseModel):
    page: Optional[int] = None
    limit: Optional[int] = None
    total: Optional[int] = None
    total_pages: Optional[int] = None


class StandardResponse(BaseModel, Generic[T]):
    success: bool
    message: str
    data: Optional[T] = None
    meta: Optional[Meta] = None