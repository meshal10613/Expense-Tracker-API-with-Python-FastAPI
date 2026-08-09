from fastapi import APIRouter, HTTPException
import json
from starlette import status

from app.config import DB_EXPENSES_FILE
from app.shared.response import Error, Success

router = APIRouter(prefix="/expenses", tags=["expenses"])


def load_data():
    with open(DB_EXPENSES_FILE, "r") as file:
        return json.load(file)


@router.get("/", response_model=Success[list[dict]], status_code=status.HTTP_200_OK)
def get_expenses():
    data = load_data()

    return Success(
        success=True, message="Expenses retrieved successfully", data=list(data.values())
    )


@router.get(
    "/{expense_id}", response_model=Success[dict], status_code=status.HTTP_200_OK
)
def get_expense(expense_id: str):
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
