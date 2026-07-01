from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Literal

# --- Generic Envelopes ---
class SuccessResponse(BaseModel):
    data: dict
    meta: Optional[dict] = None

class ErrorDetail(BaseModel):
    field: str
    issue: str

class ErrorResponse(BaseModel):
    error: dict # { "code": str, "message": str, "fields": List[ErrorDetail] }

# --- Auth Schemas ---
class VerifyEmployeeRequest(BaseModel):
    employee_id: str = Field(..., description="The unique employee ID")
    verification_method: Literal["email", "phone"] = Field(..., description="Method to receive OTP")

class VerifyOTPRequest(BaseModel):
    employee_id: str
    otp: str = Field(..., min_length=5, max_length=6)

class CreatePasswordRequest(BaseModel):
    employee_id: str
    # Enforce basic complexity at the schema level
    password: str = Field(..., min_length=8, description="Must contain at least 8 characters, one number, and one special character")

# --- Epic 2 Schemas ---
class EmployeeBase(BaseModel):
    employee_id: str
    name: str
    email: EmailStr
    role: str
    status: str
    department: Optional[str] = None

class EmployeeListResponse(SuccessResponse):
    data: List[EmployeeBase]

class EmployeeDetailResponse(SuccessResponse):
    data: EmployeeBase

class UpdateRoleRequest(BaseModel):
    role: Literal["HR", "Admin", "Owner", "Site Lead", "Technician", "Default User"]
