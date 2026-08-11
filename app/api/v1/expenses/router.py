from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Path, Query
from starlette import status

from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse
from app.services import expense_service
from app.shared.response import Success

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=Success[list[ExpenseResponse]], status_code=status.HTTP_200_OK)
def get_expenses(
    search: Optional[str] = Query(
        None, description="Search expenses by name, category, or description (case-insensitive)"
    ),
    sort_by: Optional[str] = Query(
        None,
        description="Field to sort expenses by (e.g. name, amount, date, category)",
    ),
    order: Optional[Literal["asc", "desc"]] = Query(
        "asc", description="Sort order: 'asc' or 'desc'"
    ),
):
    allowed_sort_fields = {"id", "name", "amount", "category", "date", "description"}
    if sort_by is not None and sort_by.strip():
        sort_field = sort_by.strip()
        if sort_field not in allowed_sort_fields:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid sort field '{sort_field}'. Allowed fields: {', '.join(sorted(allowed_sort_fields))}",
            )

    expenses = expense_service.get_all_expenses(search=search, sort_by=sort_by, order=order)

    return Success(
        success=True,
        message="Expenses retrieved successfully",
        data=expenses,
    )


@router.get(
    "/{expense_id}", response_model=Success[ExpenseResponse], status_code=status.HTTP_200_OK
)
def get_expense(
    expense_id: str = Path(
        ..., description="The ID of the expense to retrieve", examples=["E001"]
    )
):
    expense = expense_service.get_expense_by_id(expense_id)
    if not expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )

    return Success(
        success=True,
        message=f"Expense with ID {expense_id} retrieved successfully",
        data=expense,
    )


@router.post("/", response_model=Success[ExpenseResponse], status_code=status.HTTP_201_CREATED)
def create_expense(expense_in: ExpenseCreate):
    expense_id, created_expense = expense_service.create_expense(expense_in)

    return Success(
        success=True,
        message=f"Expense created successfully with ID {expense_id}",
        data=created_expense,
    )


@router.put(
    "/{expense_id}", response_model=Success[ExpenseResponse], status_code=status.HTTP_200_OK
)
def update_expense(
    expense_in: ExpenseUpdate,
    expense_id: str = Path(
        ..., description="The ID of the expense to update", examples=["E001"]
    ),
):
    updated_expense = expense_service.update_expense(expense_id, expense_in)
    if not updated_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )

    return Success(
        success=True,
        message=f"Expense with ID {expense_id} updated successfully",
        data=updated_expense,
    )


@router.delete(
    "/{expense_id}", response_model=Success[ExpenseResponse], status_code=status.HTTP_200_OK
)
def delete_expense(
    expense_id: str = Path(
        ..., description="The ID of the expense to delete", examples=["E001"]
    )
):
    deleted_expense = expense_service.delete_expense(expense_id)
    if not deleted_expense:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Expense with ID {expense_id} not found",
        )

    return Success(
        success=True,
        message=f"Expense with ID {expense_id} deleted successfully",
        data=deleted_expense,
    )
