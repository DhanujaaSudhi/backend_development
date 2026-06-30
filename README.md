# 8stages

## Error Handling & CORS Implementation

### Overview
This implementation adds comprehensive error handling and CORS (Cross-Origin Resource Sharing) support to the FastAPI application, following FastAPI best practices.

### Error Handling

#### HTTPException
Routes use HTTPException for error responses:

```python
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep) -> HeroPublic:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero
```

#### Custom Exception Handlers
Custom handlers provide standardized error responses:

**Validation Error Handler:**
```python
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Invalid input data",
                "details": exc.errors()
            },
            "meta": {
                "timestamp": "2024-06-30T00:00:00Z",
                "version": "v1"
            }
        }
    )
```

**HTTP Exception Handler:**
```python
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": "HTTP_ERROR",
                "message": exc.detail
            },
            "meta": {
                "timestamp": "2024-06-30T00:00:00Z",
                "version": "v1"
            }
        }
    )
```

### CORS Configuration

CORS middleware allows cross-origin requests from specified origins:

```python
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
    "http://127.0.0.1",
    "http://127.0.0.1:8080",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error Response Examples

**Validation Error (422):**
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "type": "missing",
        "loc": ["body", "secret_name"],
        "msg": "Field required",
        "input": {"name": "Test"}
      }
    ]
  },
  "meta": {
    "timestamp": "2024-06-30T00:00:00Z",
    "version": "v1"
  }
}
```

**HTTP Error (404):**
```json
{
  "error": {
    "code": "HTTP_ERROR",
    "message": "Hero not found"
  },
  "meta": {
    "timestamp": "2024-06-30T00:00:00Z",
    "version": "v1"
  }
}
```

### Benefits

**Error Handling:**
- Consistent error format across all endpoints
- Detailed validation error information
- Standardized error codes
- Metadata for tracking and debugging

**CORS:**
- Enables frontend-backend communication
- Supports credentials (cookies, auth headers)
- Configurable allowed origins
- Security through explicit origin whitelisting

### Testing

**Test Validation Error:**
```bash
curl -X POST http://127.0.0.1:8001/heroes/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'
```

**Test HTTP Error:**
```bash
curl http://127.0.0.1:8001/heroes/999
```

**Test CORS:**
Frontend applications can now make requests from allowed origins without CORS errors.

---

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

---

## Stage 3: SQL Database Integration with SQLModel and Alembic

### Overview
This stage implements SQL database integration using SQLModel (built on SQLAlchemy and Pydantic) and Alembic for database migrations. The application now persists data in a SQLite database with proper CRUD operations, model separation for security, and database version control.

### Implementation Details

#### SQLModel Models
- **HeroBase**: Base model with shared fields (name, age)
- **Hero**: Table model with database-specific fields (id, secret_name)
- **HeroPublic**: Public response model (excludes secret_name for security)
- **HeroCreate**: Request model for creating heroes (includes secret_name)
- **HeroUpdate**: Request model for updating heroes (all fields optional)

#### Database Setup
- **SQLite Database**: Single-file database for simplicity (database.db)
- **Engine**: SQLAlchemy engine for database connections
- **Session Dependency**: FastAPI dependency providing database session per request
- **Startup Event**: Automatic table creation on application startup

#### Alembic Migrations
- **Migration Environment**: Initialized with `alembic init alembic`
- **Configuration**: Database URL configured in alembic.ini
- **Autogenerate**: Automatic migration generation from SQLModel models
- **Version Control**: Database schema changes tracked with migration files

### API Endpoints

#### POST /heroes/
Create a new hero.

**Request Body:**
```json
{
  "name": "string",
  "age": 0,
  "secret_name": "string"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "age": 0
}
```

#### GET /heroes/
Retrieve a list of heroes with pagination.

**Query Parameters:**
- `offset` (default: 0): Number of heroes to skip
- `limit` (default: 100, max: 100): Maximum number of heroes to return

**Response:**
```json
[
  {
    "id": 1,
    "name": "Deadpond",
    "age": 30
  }
]
```

#### GET /heroes/{hero_id}
Retrieve a specific hero by ID.

**Parameters:**
- `hero_id` (path parameter): Integer ID of the hero

**Response:**
```json
{
  "id": 1,
  "name": "Deadpond",
  "age": 30
}
```

#### PATCH /heroes/{hero_id}
Update a hero. Only provided fields are updated.

**Request Body:**
```json
{
  "name": "string (optional)",
  "age": 0 (optional),
  "secret_name": "string (optional)"
}
```

**Response:**
```json
{
  "id": 1,
  "name": "string",
  "age": 0
}
```

#### DELETE /heroes/{hero_id}
Delete a hero by ID.

**Response:**
```json
{
  "ok": true
}
```

### Key Concepts Implemented

1. **SQLModel**: Combines Pydantic and SQLAlchemy for type-safe database models
2. **Table Models**: Models with `table=True` represent database tables
3. **Data Models**: Models without `table=True` for request/response validation
4. **Model Inheritance**: Reusing fields through base classes to avoid duplication
5. **Database Indexes**: Using `Field(index=True)` for optimized queries
6. **Session Management**: FastAPI dependency for database session per request
7. **Security**: Separating public/private models to hide sensitive data (secret_name)
8. **CRUD Operations**: Create, Read, Update, Delete operations with proper error handling
9. **Alembic Migrations**: Database schema version control and migration management
10. **Autogenerate**: Automatic migration generation from model changes

### Technical Details

- **Database**: SQLite (for development, easily switchable to PostgreSQL/MySQL)
- **ORM**: SQLModel 0.0.39 (built on SQLAlchemy 2.0.51)
- **Migration Tool**: Alembic 1.18.5
- **Session Management**: One session per request using FastAPI dependencies
- **Primary Key**: Auto-generated integer ID
- **Indexes**: Created on name and age fields for faster queries

### Setup Instructions

1. **Install additional dependencies**
   ```bash
   pip install sqlmodel alembic
   ```

2. **Initialize Alembic** (already done)
   ```bash
   alembic init alembic
   ```

3. **Configure alembic.ini** (already done)
   - Set `sqlalchemy.url = sqlite:///database.db`

4. **Update env.py** (already done)
   - Import SQLModel and models for autogenerate support
   - Set `target_metadata = SQLModel.metadata`

5. **Generate migration** (already done)
   ```bash
   alembic revision --autogenerate -m "Initial migration - create hero table"
   ```

6. **Run migration**
   ```bash
   alembic upgrade head
   ```

### Migration Commands

- **Generate new migration**: `alembic revision --autogenerate -m "description"`
- **Apply migrations**: `alembic upgrade head`
- **Rollback migration**: `alembic downgrade -1`
- **View migration history**: `alembic history`
- **View current version**: `alembic current`

### Database Schema

The Hero table structure:
- `id`: INTEGER PRIMARY KEY (auto-generated)
- `name`: TEXT (indexed)
- `age`: INTEGER (indexed, nullable)
- `secret_name`: TEXT (not null)

### Security Considerations

- **Secret Data**: The `secret_name` field is never returned in API responses
- **Model Separation**: Using separate models for input/output prevents data leakage
- **Validation**: All data is validated through Pydantic models before database operations
- **SQL Injection**: SQLModel/SQLAlchemy provides protection against SQL injection

### Benefits of This Approach

- **Type Safety**: Full type checking for database models and API contracts
- **Automatic Documentation**: API docs automatically reflect database schema
- **Migration Management**: Version-controlled database schema changes
- **Security**: Built-in protection against data exposure through model separation
- **Performance**: Database indexes on frequently queried fields
- **Flexibility**: Easy to switch between SQLite, PostgreSQL, MySQL, etc.
- **Developer Experience**: Excellent editor support with autocomplete

---

## Stage 4: Query Parameters and Path Parameters

### Overview
This stage demonstrates FastAPI's powerful parameter handling capabilities, including query parameters with defaults, optional parameters, type validation, boolean conversion, required parameters, multiple parameters, path parameters with types, enum-based predefined values, and path convertors for handling paths within paths.

### Implementation Details

#### Query Parameters
- **Default Values**: Parameters with default values (skip=0, limit=10)
- **Optional Parameters**: Parameters that can be None (q: str | None = None)
- **Boolean Conversion**: Automatic conversion of string values to bool (short: bool = False)
- **Required Parameters**: Parameters without defaults are required (needy: str)
- **Multiple Parameters**: Combining path and query parameters in a single endpoint

#### Path Parameters
- **Type Validation**: Path parameters with type annotations (item_id: int)
- **Enum Predefined Values**: Restricting path parameters to specific values using Enum
- **Path Convertor**: Handling paths that contain slashes using :path

### API Endpoints

#### GET /items/
Query parameters with default values for pagination.

**Query Parameters:**
- `skip` (default: 0): Number of items to skip
- `limit` (default: 10): Maximum number of items to return

**URL Example:** `/items/?skip=0&limit=10`

**Response:**
```json
[
  {"item_name": "Foo"},
  {"item_name": "Bar"}
]
```

#### GET /items/{item_id}
Optional query parameter.

**Parameters:**
- `item_id` (path): String ID of the item
- `q` (query, optional): Search query string

**URL Example:** `/items/foo?q=search`

**Response:**
```json
{
  "item_id": "foo",
  "q": "search"
}
```

#### GET /items/{item_id}/detail
Boolean query parameter with automatic conversion.

**Parameters:**
- `item_id` (path): String ID of the item
- `q` (query, optional): Search query string
- `short` (query, default: false): Boolean flag for short response

**URL Example:** `/items/foo/detail?short=true`

**Response (short=false):**
```json
{
  "item_id": "foo",
  "description": "This is an amazing item that has a long description"
}
```

#### GET /items/{item_id}/required
Required query parameter.

**Parameters:**
- `item_id` (path): String ID of the item
- `needy` (query, required): Required string parameter

**URL Example:** `/items/foo/required?needy=value`

**Response:**
```json
{
  "item_id": "foo",
  "needy": "value"
}
```

#### GET /users/{user_id}/items/{item_id}
Multiple path and query parameters.

**Parameters:**
- `user_id` (path): Integer user ID
- `item_id` (path): String item ID
- `q` (query, optional): Search query string
- `short` (query, default: false): Boolean flag for short response

**URL Example:** `/users/1/items/foo?q=search&short=true`

**Response:**
```json
{
  "item_id": "foo",
  "owner_id": 1,
  "q": "search"
}
```

#### GET /items/{item_id}/typed
Path parameter with type validation.

**Parameters:**
- `item_id` (path): Integer ID of the item

**URL Example:** `/items/3/typed`

**Response:**
```json
{
  "item_id": 3
}
```

#### GET /models/{model_name}
Path parameter with predefined enum values.

**Parameters:**
- `model_name` (path): One of "alexnet", "resnet", "lenet"

**URL Example:** `/models/alexnet`

**Response:**
```json
{
  "model_name": "alexnet",
  "message": "Deep Learning FTW!"
}
```

#### GET /files/{file_path:path}
Path parameter containing a path.

**Parameters:**
- `file_path` (path): File path (can contain slashes)

**URL Example:** `/files//home/johndoe/myfile.txt` (note double slash)

**Response:**
```json
{
  "file_path": "/home/johndoe/myfile.txt"
}
```

### Key Concepts Implemented

1. **Query Parameters**: Parameters in URL after ? separated by &
2. **Default Values**: Optional parameters with default values
3. **Type Conversion**: Automatic conversion from string to declared types
4. **Boolean Conversion**: Smart conversion of various string formats to bool
5. **Required Parameters**: Parameters without defaults are mandatory
6. **Optional Parameters**: Parameters with default=None are optional
7. **Multiple Parameters**: Combining path and query parameters
8. **Type Validation**: Automatic validation with clear error messages
9. **Enum Values**: Restricting parameters to predefined values
10. **Path Convertor**: Handling paths with slashes using :path
11. **Order Matters**: More specific paths must be declared before parameterized ones
12. **Automatic Documentation**: All parameters documented in Swagger UI

### Boolean Conversion Examples

FastAPI automatically converts these string values to `True`:
- `1`, `True`, `true`, `on`, `yes` (case-insensitive)

All other values convert to `False`

### Type Validation

When a type is declared, FastAPI:
- Converts the value to the specified type
- Validates the conversion
- Returns clear error messages if validation fails

**Error Example for Invalid Type:**
```json
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": ["path", "item_id"],
      "msg": "Input should be a valid integer",
      "input": "foo"
    }
  ]
}
```

### Path Ordering

More specific paths must be declared before parameterized paths:
```python
@app.get("/users/me")  # Must come first
async def read_user_me():
    return {"user_id": "the current user"}

@app.get("/users/{user_id}")  # Must come after
async def read_user(user_id: str):
    return {"user_id": user_id}
```

### Benefits of This Approach

- **Type Safety**: Automatic type conversion and validation
- **Clear Errors**: Detailed error messages for invalid inputs
- **Documentation**: Automatic API documentation with parameter details
- **Flexibility**: Support for optional, required, and default values
- **Editor Support**: Autocomplete and type checking in IDEs
- **Standards Compliance**: Based on OpenAPI specification
- **Developer Experience**: Intuitive Python-style parameter declarations