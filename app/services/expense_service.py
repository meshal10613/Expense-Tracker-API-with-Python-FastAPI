import json
from typing import Literal, Optional
from app.config import DB_EXPENSES_FILE
from app.schemas.expense import ExpenseCreate, ExpenseUpdate


def load_data() -> dict:
    with open(DB_EXPENSES_FILE, "r") as file:
        return json.load(file)


def save_data(data: dict) -> None:
    with open(DB_EXPENSES_FILE, "w") as file:
        json.dump(data, file, indent=4)


def generate_next_id(data: dict) -> str:
    existing_nums = []
    for key in data.keys():
        if key.startswith("E") and key[1:].isdigit():
            existing_nums.append(int(key[1:]))
    next_num = max(existing_nums, default=0) + 1
    return f"E{next_num:03d}"


def get_all_expenses(
    search: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: Literal["asc", "desc"] = "asc",
) -> list[dict]:
    data = load_data()
    expenses = [{"id": k, **v} for k, v in data.items()]

    if isinstance(search, str) and search.strip():
        search_term = search.strip().lower()
        expenses = [
            e
            for e in expenses
            if search_term in e.get("name", "").lower()
            or search_term in e.get("category", "").lower()
            or search_term in e.get("description", "").lower()
        ]

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
        if sort_field in allowed_sort_fields:
            is_reverse = order == "desc"
            expenses.sort(key=lambda item: item.get(sort_field, ""), reverse=is_reverse)

    return expenses


def get_expense_by_id(expense_id: str) -> Optional[dict]:
    data = load_data()
    expense = data.get(expense_id)
    if not expense:
        return None
    return {"id": expense_id, **expense}


def create_expense(expense_in: ExpenseCreate) -> tuple[str, dict]:
    data = load_data()
    expense_id = generate_next_id(data)
    expense_dict = expense_in.model_dump()

    data[expense_id] = expense_dict
    save_data(data)

    return expense_id, {"id": expense_id, **expense_dict}


def update_expense(expense_id: str, expense_in: ExpenseUpdate) -> Optional[dict]:
    data = load_data()
    if expense_id not in data:
        return None

    update_data = expense_in.model_dump(exclude_unset=True, exclude_none=True)
    data[expense_id].update(update_data)
    save_data(data)

    return {"id": expense_id, **data[expense_id]}


def delete_expense(expense_id: str) -> Optional[dict]:
    data = load_data()
    if expense_id not in data:
        return None

    deleted_expense = data.pop(expense_id)
    save_data(data)

    return {"id": expense_id, **deleted_expense}
