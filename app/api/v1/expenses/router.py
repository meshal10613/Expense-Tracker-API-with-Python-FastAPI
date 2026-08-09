from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Path, Query
import json
from starlette import status

from app.config import DB_EXPENSES_FILE
from app.shared.response import Error, Success

router = APIRouter(prefix="/expenses", tags=["expenses"])


def load_data():
    with open(DB_EXPENSES_FILE, "r") as file:
        return json.load(file)


@router.get("/", response_model=Success[list[dict]], status_code=status.HTTP_200_OK)
def get_expenses(
    search: Optional[str] = Query(
        None, description="Search expenses by name (case-insensitive)"
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort expenses by (e.g. name, amount, date, category)",
    ),
    order: Optional[Literal["asc", "desc"]] = Query(
        "asc", description="Sort order: 'asc' or 'desc'"
    ),
):
    data = load_data()
    expenses = [{"id": k, **v} for k, v in data.items()]

    if isinstance(search, str) and search.strip():
        search_term = search.strip().lower()
        expenses = [e for e in expenses if search_term in e.get("name", "").lower()]

    if isinstance(sort_by, str) and sort_by.strip():
        sort_field = sort_by.strip()
        allowed_sort_fields = {
            "id",
            "name",
            "amount",
            "category",
            "date",
            "description",
        }
        if sort_field not in allowed_sort_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field '{sort_field}'. Allowed fields: {', '.join(sorted(allowed_sort_fields))}",
            )
        is_reverse = order == "desc"
        expenses.sort(key=lambda item: item.get(sort_field, ""), reverse=is_reverse)

    return Success(
        success=True,
        message="Expenses retrieved successfully",
        data=expenses,
    )


@router.get(
    "/{expense_id}", response_model=Success[dict], status_code=status.HTTP_200_OK
)
def get_expense(
    expense_id: str = Path(
        ..., description="The ID of the expense to retrieve", examples=["E001"]
    )
):
    data = load_data()
    expense = data.get(expense_id)

    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )

    return Success(
        success=True,
        message=f"Expense with ID {expense_id} retrieved successfully",
        data={"expense": expense},
    )
