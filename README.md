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