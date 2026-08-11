from datetime import date as date_type
from typing import Annotated, Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class ExpenseBase(BaseModel):
    name: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="Name of the expense",
            examples=["Groceries"],
        ),
    ]
    amount: Annotated[
        float,
        Field(
            gt=0,
            description="Amount spent (must be greater than 0)",
            examples=[150.75],
        ),
    ]
    category: Annotated[
        str,
        Field(
            min_length=1,
            max_length=50,
            description="Category of the expense",
            examples=["Food"],
        ),
    ]
    description: Annotated[
        str,
        Field(
            max_length=500,
            description="Detailed description of the expense",
            examples=["Weekly grocery shopping at the local supermarket."],
        ),
    ]


class ExpenseCreate(ExpenseBase):
    date: Annotated[
        Optional[str],
        Field(
            default_factory=lambda: date_type.today().isoformat(),
            description="ISO date format (YYYY-MM-DD). Auto-generated if omitted.",
            examples=["2026-08-11"],
        ),
    ]

    @field_validator("date", mode="before")
    @classmethod
    def validate_and_default_date(cls, v: Optional[str]) -> str:
        if v is None or (isinstance(v, str) and not v.strip()):
            return date_type.today().isoformat()
        if isinstance(v, str):
            v_clean = v.strip()
            try:
                date_type.fromisoformat(v_clean)
            except ValueError:
                raise ValueError("Date must be in valid YYYY-MM-DD format.")
            return v_clean
        return v


class ExpenseUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=100,
            description="Updated name of the expense",
        ),
    ] = None

    amount: Annotated[
        Optional[float],
        Field(
            default=None,
            gt=0,
            description="Updated amount (must be greater than 0)",
        ),
    ] = None

    category: Annotated[
        Optional[str],
        Field(
            default=None,
            min_length=1,
            max_length=50,
            description="Updated category",
        ),
    ] = None

    date: Annotated[
        Optional[str],
        Field(
            default=None,
            description="Updated ISO date (YYYY-MM-DD)",
        ),
    ] = None

    description: Annotated[
        Optional[str],
        Field(
            default=None,
            max_length=500,
            description="Updated description",
        ),
    ] = None

    @field_validator("date")
    @classmethod
    def validate_date_format(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            v_clean = v.strip()
            try:
                date_type.fromisoformat(v_clean)
            except ValueError:
                raise ValueError("Date must be in valid YYYY-MM-DD format.")
            return v_clean
        return v

    @model_validator(mode="after")
    def validate_at_least_one_field(self) -> "ExpenseUpdate":
        fields_set = self.model_dump(exclude_unset=True)
        non_null_fields = {k: v for k, v in fields_set.items() if v is not None}
        if not non_null_fields:
            raise ValueError("At least one field must be provided for update.")
        return self


class ExpenseResponse(BaseModel):
    id: Annotated[str, Field(description="Unique expense ID", examples=["E001"])]
    name: Annotated[str, Field(examples=["Groceries"])]
    amount: Annotated[float, Field(examples=[150.75])]
    category: Annotated[str, Field(examples=["Food"])]
    date: Annotated[str, Field(examples=["2026-08-11"])]
    description: Annotated[
        str,
        Field(examples=["Weekly grocery shopping at the local supermarket."]),
    ]
