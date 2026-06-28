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

## Stage 2: Request Body & Response Models

### Overview
This stage implements Pydantic models for request body validation and response model filtering. The application demonstrates proper data validation, automatic documentation generation, and security best practices by separating input and output models.

### Implementation Details

#### Pydantic Models
- **ItemBase**: Base model with common item fields (name, description, price, tax)
- **ItemCreate**: Request model for creating items (inherits from ItemBase)
- **ItemResponse**: Response model with additional fields (id, price_with_tax)
- **UserBase**: Base model with common user fields (username, email, full_name)
- **UserIn**: Request model for user creation (includes password)
- **UserOut**: Response model for user data (excludes password for security)

#### New Endpoints
- **POST /items/**: Create a new item with automatic tax calculation
- **GET /items/{item_id}**: Retrieve an item by ID
- **POST /user/**: Create a new user (password not returned in response)

### API Endpoints

#### POST /items/
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
  "id": 1,
  "name": "string",
  "description": "string",
  "price": 0.0,
  "tax": 0.0,
  "price_with_tax": 0.0
}
```

#### GET /items/{item_id}
Retrieve an item by ID.

**Parameters:**
- `item_id` (path parameter): Integer ID of the item

**Response:**
```json
{
  "id": 1,
  "name": "Sample Item",
  "description": "A sample item description",
  "price": 99.99,
  "tax": 8.99,
  "price_with_tax": 108.98
}
```

#### POST /user/
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
  "username": "string",
  "email": "user@example.com",
  "full_name": "string"
}
```

#### POST /items/with-tags/
Create an item with tags using return type annotation.

**Request Body:**
```json
{
  "name": "string",
  "description": "string (optional)",
  "price": 0.0,
  "tax": 0.0 (optional),
  "tags": ["string"]
}
```

**Response:**
```json
{
  "name": "string",
  "description": "string",
  "price": 0.0,
  "tax": 0.0,
  "tags": ["string"]
}
```

#### GET /items/list/
Return a list of items using return type annotation.

**Response:**
```json
[
  {
    "name": "Portal Gun",
    "description": null,
    "price": 42.0,
    "tax": null,
    "tags": ["sci-fi", "weapon"]
  },
  {
    "name": "Plumbus",
    "description": null,
    "price": 32.0,
    "tax": null,
    "tags": ["household", "tool"]
  }
]
```

#### GET /items/{item_id}/minimal
Return item excluding unset default values using `response_model_exclude_unset=True`.

**Response for "foo":**
```json
{
  "name": "Foo",
  "price": 50.2
}
```

**Response for "bar":**
```json
{
  "name": "Bar",
  "description": "The bartenders",
  "price": 62,
  "tax": 20.2
}
```

#### GET /items/{item_id}/name-only
Return item with only name and description fields using `response_model_include`.

**Response:**
```json
{
  "name": "string",
  "description": "string"
}
```

#### GET /items/{item_id}/public
Return item excluding tax field using `response_model_exclude`.

**Response:**
```json
{
  "name": "string",
  "description": "string",
  "price": 0.0,
  "tags": []
}
```

### Key Concepts Implemented

1. **Pydantic BaseModel**: Data validation using Python type annotations
2. **Request Body**: POST/PUT endpoints with structured JSON input
3. **Response Model**: Filtering output data using `response_model` parameter
4. **Model Inheritance**: Reusing common fields through base classes
5. **Security**: Separating input/output models to exclude sensitive data (passwords)
6. **Email Validation**: Using `EmailStr` for email field validation
7. **Automatic Documentation**: Request/response schemas automatically appear in Swagger UI
8. **Data Transformation**: Computing derived fields (price_with_tax) in responses
9. **Return Type Annotations**: Using function return types for validation and documentation
10. **response_model_exclude_unset**: Returning only explicitly set values, excluding defaults
11. **response_model_include**: Including only specific fields in the response
12. **response_model_exclude**: Excluding specific fields from the response

### Technical Details

- **Additional Dependencies**: email-validator (for EmailStr support)
- **Validation**: Automatic request validation with clear error messages
- **Documentation**: Complete OpenAPI schema with request/response examples
- **Type Safety**: Full editor support with autocomplete and type checking

### Postman Mock Server Setup

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
- **Type Safety**: Catches data type errors at development time
- **Automatic Documentation**: Always up-to-date API documentation
- **Security**: Prevents accidental exposure of sensitive data
- **Validation**: Ensures data integrity before processing
- **Developer Experience**: Excellent editor support with autocomplete