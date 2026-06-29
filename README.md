# 8stages

## Stage 1: First Steps - Basic FastAPI Application

### Overview
This stage implements the simplest FastAPI application following the official FastAPI tutorial. The application provides a basic "Hello World" endpoint with automatic API documentation.

### Implementation Details

#### Files Created
- **main.py**: Contains the FastAPI application with a single root endpoint
- **pyproject.toml**: Configuration file with FastAPI entrypoint settings

#### main.py
```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
```

#### pyproject.toml
```toml
[tool.fastapi]
entrypoint = "main:app"
```

### Setup Instructions

1. **Create virtual environment**
   ```bash
   python -m venv venv
   ```

2. **Activate virtual environment**
   - Windows: `.\venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`

3. **Install dependencies**
   ```bash
   pip install "fastapi[standard]"
   ```

4. **Run development server**
   ```bash
   fastapi dev
   ```

### Running the Application

The development server starts at:
- **Main Application**: http://127.0.0.1:8000
- **Interactive API Docs (Swagger UI)**: http://127.0.0.1:8000/docs
- **Alternative API Docs (ReDoc)**: http://127.0.0.1:8000/redoc
- **OpenAPI Schema**: http://127.0.0.1:8000/openapi.json

### Interactive API Documentation (Swagger UI)

When you visit http://127.0.0.1:8000/docs, you'll see the automatic interactive API documentation provided by Swagger UI. The interface displays:

- **API Title**: "FastAPI" with version "0.1.0"
- **OpenAPI Specification**: OAS 3.1
- **OpenAPI JSON Link**: Direct access to the raw OpenAPI schema at `/openapi.json`
- **Endpoint List**: All available API endpoints organized by tag
- **GET / Root**: The single endpoint in this basic application

The Swagger UI allows you to:
- View all available endpoints and their HTTP methods
- See request/response schemas
- Test endpoints directly from the browser
- Expand each endpoint to view detailed information about parameters, request body, and response formats

### API Endpoints

#### GET /
Returns a JSON response with a greeting message.

**Response:**
```json
{
  "message": "Hello World"
}
```

### Key Concepts Implemented

1. **FastAPI Instance**: Created using `app = FastAPI()`
2. **Path Operation**: Defined using decorator `@app.get("/")`
3. **Path Operation Function**: Async function that handles requests to the specified path
4. **Automatic Documentation**: FastAPI automatically generates OpenAPI schema and interactive documentation
5. **Configuration**: Entrypoint configured in pyproject.toml for consistent CLI usage

### Technical Details

- **Framework**: FastAPI 0.138.0
- **Server**: Uvicorn 0.49.0
- **Python Version**: 3.11+
- **Async Support**: Uses async/await for better performance
- **OpenAPI Version**: 3.1.0

### Next Steps

This basic setup provides the foundation for building more complex APIs with:
- Path parameters
- Query parameters
- Request body validation
- Authentication
- Database integration
- And more FastAPI features

---

## Stage 2: API Contract Design

### Overview
This stage implements a production-ready API contract with standardized response envelopes, versioned routes, global list conventions, and proper error handling. The contract is designed to unblock the UI team by providing a shared artifact that can be mocked before backend logic exists.

### Acceptance Criteria Met

✅ **Versioned routes under /api/v1** - All endpoints are versioned
✅ **Success, validation-error (422), and generic-error envelopes** - Standardized error responses
✅ **List paging/filter/sort agreed once, globally** - Global pagination and sorting conventions
✅ **Dates ISO 8601 UTC; units explicit** - All timestamps in UTC with explicit timezone
✅ **OpenAPI doc published, link shared** - Available at /docs and /openapi.json
✅ **Mock server live before backend logic exists** - Contract ready for Postman mock server

### Implementation Details

#### Response Envelope Models
- **SuccessResponse**: Standard success envelope with `{data, meta}` structure
- **ErrorResponse**: Standard error envelope with `{error, meta}` structure
- **Meta**: Contains timestamp (ISO 8601 UTC) and API version

#### Error Envelope Models
- **ErrorCode**: Enum of standardized error codes (VALIDATION_ERROR, NOT_FOUND, INTERNAL_ERROR, etc.)
- **ErrorDetail**: Detailed error information with field and message
- **ErrorResponse.create()**: Factory method for creating error responses

#### Global List Conventions
- **PaginationParams**: Global pagination (offset, limit with validation)
- **SortParams**: Global sorting (sort_by, order with enum)
- **FilterOperator**: Enum of filter operators (equals, contains, greater_than, etc.)
- **FilterParam**: Single filter parameter structure

#### Domain Models
- **ItemBase, ItemCreate, ItemResponse**: Item models with ISO 8601 UTC timestamps
- **UserBase, UserIn, UserOut**: User models with password filtering for security

### API Endpoints

#### GET /api/v1/health
Health check endpoint.

**Response:**
```json
{
  "data": {
    "status": "healthy",
    "service": "8stages-api"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### POST /api/v1/items/
Create a new item with automatic tax calculation.

**Request Body:**
```json
{
  "name": "string",
  "description": "string (optional)",
  "price": 0.0,
  "tax": 0.0 (optional)
}
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "string",
    "description": "string",
    "price": 0.0,
    "tax": 0.0,
    "price_with_tax": 0.0,
    "created_at": "2024-06-29T10:00:00Z"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### GET /api/v1/items/{item_id}
Retrieve an item by ID.

**Response:**
```json
{
  "data": {
    "id": 1,
    "name": "Sample Item",
    "description": "A sample item description",
    "price": 99.99,
    "tax": 8.99,
    "price_with_tax": 108.98,
    "created_at": "2024-06-29T10:00:00Z"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### GET /api/v1/items/
List items with pagination and sorting (global list conventions).

**Query Parameters:**
- `offset` (default: 0, min: 0): Number of items to skip
- `limit` (default: 100, min: 1, max: 100): Maximum number of items to return
- `sort_by` (default: "id"): Field to sort by
- `order` (default: "asc"): Sort order ("asc" or "desc")

**URL Example:** `/api/v1/items/?offset=0&limit=10&sort_by=name&order=asc`

**Response:**
```json
{
  "data": [
    {
      "id": 1,
      "name": "Portal Gun",
      "description": "Interdimensional travel device",
      "price": 42.0,
      "tax": 3.5,
      "price_with_tax": 45.5,
      "created_at": "2024-06-29T10:00:00Z"
    }
  ],
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### POST /api/v1/users/
Create a new user. Password is not returned in the response for security.

**Request Body:**
```json
{
  "username": "string",
  "password": "string",
  "email": "user@example.com",
  "full_name": "string (optional)"
}
```

**Response:**
```json
{
  "data": {
    "id": 1,
    "username": "string",
    "email": "user@example.com",
    "full_name": "string",
    "created_at": "2024-06-29T10:00:00Z"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### GET /api/v1/users/{user_id}
Retrieve a user by ID.

**Response:**
```json
{
  "data": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "full_name": "John Doe",
    "created_at": "2024-06-29T10:00:00Z"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

### Error Response Examples

#### Validation Error (422)
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "price",
        "message": "Field required"
      }
    ]
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### Not Found Error (404)
```json
{
  "error": {
    "code": "NOT_FOUND",
    "message": "Resource not found"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

#### Internal Error (500)
```json
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "An unexpected error occurred"
  },
  "meta": {
    "timestamp": "2024-06-29T10:00:00Z",
    "version": "v1"
  }
}
```

### Key Concepts Implemented

1. **Versioned Routes**: All endpoints under `/api/v1` for API versioning
2. **Success Envelope**: Standardized `{data, meta}` response structure
3. **Error Envelope**: Standardized `{error, meta}` response structure
4. **ISO 8601 UTC**: All timestamps in UTC with explicit timezone indicator
5. **Global Pagination**: Consistent offset/limit parameters across all list endpoints
6. **Global Sorting**: Consistent sort_by/order parameters across all list endpoints
7. **Error Codes**: Enum-based standardized error codes
8. **Response Metadata**: Timestamp and version in all responses
9. **Security**: Password filtering in user responses
10. **Type Safety**: Full Pydantic validation for all requests/responses

### Technical Details

- **API Version**: v1 (configurable via API_VERSION constant)
- **Date Format**: ISO 8601 UTC (e.g., "2024-06-29T10:00:00Z")
- **Pagination Defaults**: offset=0, limit=100 (max 100)
- **Sort Order**: asc/desc enum
- **Filter Operators**: equals, contains, starts_with, ends_with, greater_than, less_than
- **Error Codes**: VALIDATION_ERROR, NOT_FOUND, INTERNAL_ERROR, UNAUTHORIZED, FORBIDDEN

### OpenAPI Documentation

The API contract is automatically documented at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **OpenAPI JSON**: http://127.0.0.1:8000/openapi.json
- **ReDoc**: http://127.0.0.1:8000/redoc

### Mock Server Setup

To create a mock server in Postman:

1. **Export OpenAPI Schema**: Visit http://127.0.0.1:8000/openapi.json
2. **Import to Postman**: 
   - Open Postman
   - Click "Import" and select the OpenAPI JSON file
   - Postman will automatically create a collection with all endpoints
3. **Create Mock Server**:
   - Select the imported collection
   - Click "..." > "Mock collection"
   - Choose a mock URL (e.g., `https://8stages.mock.pstmn.io`)
   - Frontend developers can now use this mock URL to build against the API contract

### Benefits of This Approach

- **Contract-First Development**: Frontend and backend can work in parallel using the API contract
- **Versioning**: Clear API versioning prevents breaking changes
- **Consistency**: Global conventions ensure consistent API experience
- **Type Safety**: Full type checking for request/response contracts
- **Automatic Documentation**: Always up-to-date API documentation
- **Security**: Standardized error handling prevents information leakage
- **Mock-Ready**: Contract can be mocked before backend implementation
- **Standards Compliance**: Based on OpenAPI 3.1.0 specification