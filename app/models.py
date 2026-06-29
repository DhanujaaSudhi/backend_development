from datetime import datetime, timezone
from typing import Any, Generic, TypeVar
from enum import Enum

from pydantic import BaseModel, EmailStr, Field

# API Version
API_VERSION = "v1"

# Generic Type for Response Data
T = TypeVar("T")

# Response Envelope Models
class Meta(BaseModel):
    """Metadata for API responses"""
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    version: str = API_VERSION


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response envelope"""
    data: T
    meta: Meta = Field(default_factory=Meta)


# Error Envelope Models
class ErrorCode(str, Enum):
    """Standardized error codes"""
    VALIDATION_ERROR = "VALIDATION_ERROR"
    NOT_FOUND = "NOT_FOUND"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"


class ErrorDetail(BaseModel):
    """Detailed error information"""
    field: str | None = None
    message: str


class ErrorResponse(BaseModel):
    """Standard error response envelope"""
    error: dict
    meta: Meta = Field(default_factory=Meta)

    @classmethod
    def create(cls, code: ErrorCode, message: str, details: list[ErrorDetail] | None = None):
        """Factory method to create error response"""
        error_dict = {
            "code": code.value,
            "message": message
        }
        if details:
            error_dict["details"] = [d.model_dump() for d in details]
        return cls(error=error_dict)


# Pagination and Filter Models
class SortOrder(str, Enum):
    """Sort order options"""
    asc = "asc"
    desc = "desc"


class PaginationParams(BaseModel):
    """Global pagination parameters"""
    offset: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=100, ge=1, le=100, description="Maximum number of items to return")


class SortParams(BaseModel):
    """Global sort parameters"""
    sort_by: str = Field(default="id", description="Field to sort by")
    order: SortOrder = Field(default=SortOrder.asc, description="Sort order")


class FilterOperator(str, Enum):
    """Filter operators"""
    equals = "equals"
    contains = "contains"
    starts_with = "starts_with"
    ends_with = "ends_with"
    greater_than = "greater_than"
    less_than = "less_than"


class FilterParam(BaseModel):
    """Single filter parameter"""
    field: str
    operator: FilterOperator = FilterOperator.equals
    value: str


# Domain Models
class ItemBase(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    id: int
    price_with_tax: float | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    id: int
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
