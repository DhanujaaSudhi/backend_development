from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from schemas import (
    VerifyEmployeeRequest, VerifyOTPRequest, CreatePasswordRequest,
    SuccessResponse, ErrorResponse, UpdateRoleRequest
)

description = """
esysflow Core Employee Hub API helps you manage employee authentication and records. 🚀

## Auth
You can **verify employees**, **verify OTPs**, and **create passwords**.

## Employees
You will be able to:
* **Read employees** with pagination.
* **Read specific employee details**.
* **Update employee roles**.
"""

tags_metadata = [
    {
        "name": "auth",
        "description": "Operations with authentication. The **login** logic is here.",
    },
    {
        "name": "employees",
        "description": "Manage employees and their details.",
        "externalDocs": {
            "description": "Employees external docs",
            "url": "https://esysflow.example.com/docs/employees",
        },
    },
]

app = FastAPI(
    title="esysflow Core Employee Hub",
    description=description,
    summary="Core Employee Management API for esysflow.",
    version="1.0.0",
    terms_of_service="http://esysflow.example.com/terms/",
    contact={
        "name": "esysflow API Support",
        "url": "http://esysflow.example.com/contact/",
        "email": "support@esysflow.example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "identifier": "Apache-2.0",
    },
    openapi_tags=tags_metadata,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS configuration (Stage 6)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to the frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/auth/verify-employee", response_model=SuccessResponse, status_code=status.HTTP_200_OK, tags=["auth"])
async def verify_employee(request: VerifyEmployeeRequest):
    """
    Step 1: User enters Employee ID and chooses Email or Phone.
    System checks DB for exact match and generates an OTP if found.
    """
    # MOCK LOGIC for Stage 2
    if request.employee_id == "INVALID":
        raise HTTPException(status_code=404, detail="Information does not match our records")
    
    return SuccessResponse(data={"message": f"OTP sent successfully to registered {request.verification_method}"})

@app.post("/api/v1/auth/verify-otp", response_model=SuccessResponse, status_code=status.HTTP_200_OK, tags=["auth"])
async def verify_otp(request: VerifyOTPRequest):
    """
    Step 2: User submits the OTP they received.
    """
    # MOCK LOGIC for Stage 2
    if request.otp != "12345":
        raise HTTPException(status_code=400, detail="Invalid OTP")
        
    return SuccessResponse(data={"message": "OTP verified successfully. Proceed to password creation."})

@app.post("/api/v1/auth/create-password", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED, tags=["auth"])
async def create_password(request: CreatePasswordRequest):
    """
    Step 3: User creates a secure password.
    """
    # MOCK LOGIC for Stage 2
    return SuccessResponse(data={"message": "Password created successfully", "token": "mock_jwt_token"})

# --- Epic 2: Employee Directory ---
from typing import Optional

@app.get("/api/v1/employees", response_model=SuccessResponse, status_code=status.HTTP_200_OK, tags=["employees"])
async def get_employees(page: int = 1, size: int = 10, role: Optional[str] = None, department: Optional[str] = None):
    """
    Step 2.1: View Employee Directory with pagination and filtering.
    """
    # Stage 8 Demo Data
    if department == "empty_demo":
        return SuccessResponse(data={"employees": []}, meta={"page": page, "size": size, "total": 0})

    mock_employees = [
        {"employee_id": "EMP100", "name": "Alice Admin", "email": "alice@company.com", "role": "Admin", "status": "Active", "department": "HR"},
        {"employee_id": "EMP101", "name": "Bob Tech", "email": "bob@company.com", "role": "Technician", "status": "Active", "department": "Maintenance"},
        {"employee_id": "EMP102", "name": "Hubert Blaine Wolfeschlegelsteinhausenbergerdorff Sr.", "email": "hubert@company.com", "role": "User", "status": "Active", "department": "Engineering"}
    ]
    return SuccessResponse(
        data={"employees": mock_employees},
        meta={"page": page, "size": size, "total": 3}
    )

@app.get("/api/v1/employees/{employee_id}", response_model=SuccessResponse, status_code=status.HTTP_200_OK, tags=["employees"])
async def get_employee_detail(employee_id: str):
    """
    Step 2.2: View Employee Details.
    """
    if employee_id == "INVALID":
        raise HTTPException(status_code=404, detail="Employee not found")
        
    mock_employee = {"employee_id": employee_id, "name": "Alice Admin", "email": "alice@company.com", "role": "Admin", "status": "Active", "department": "HR"}
    return SuccessResponse(data={"employee": mock_employee})

@app.patch("/api/v1/employees/{employee_id}/role", response_model=SuccessResponse, status_code=status.HTTP_200_OK, tags=["employees"])
async def update_employee_role(employee_id: str, request: UpdateRoleRequest):
    """
    Step 2.3: Assign/Update Role.
    """
    if employee_id == "INVALID":
        raise HTTPException(status_code=404, detail="Employee not found")
        
    return SuccessResponse(data={"message": f"Role updated to {request.role} successfully", "employee_id": employee_id})
