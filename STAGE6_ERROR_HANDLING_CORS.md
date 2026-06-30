# Stage 6: Error Handling, Standardized Responses & CORS

## Objective
Implement predictable error handling with a global exception handler, standardized error responses, and CORS configuration to ensure the API is reachable from browsers and fails gracefully.

## Acceptance Criteria
- Global handler returns the single error envelope
- No stack traces leak; clean 500 on failure
- Correct status codes (201/200/204/401/403/404/422)
- CORS allows frontend origin, methods, headers, credentials

## Implementation

### Global Exception Handlers

**Validation Error Handler (422):**
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

### Standardized Error Envelope

All errors follow the same structure:
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": [...]  // Optional for validation errors
  },
  "meta": {
    "timestamp": "ISO 8601 UTC",
    "version": "v1"
  }
}
```

### Status Codes Used

| Code | Usage |
|------|-------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (resource created) |
| 204 | Successful DELETE (no content) |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Internal server error (clean, no stack traces) |

## Error Response Examples

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

**Not Found Error (404):**
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

## Benefits

**Error Handling:**
- Consistent error format across all endpoints
- No stack traces leaked to clients
- Clean 500 errors for internal failures
- Detailed validation errors for debugging

**CORS:**
- Frontend can communicate with backend
- Supports credentials (cookies, auth headers)
- Explicit origin whitelisting for security
- Prevents CORS-related failures

## Testing

**Test Validation Error:**
```bash
curl -X POST http://127.0.0.1:8001/heroes/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Test"}'
```

**Test 404 Error:**
```bash
curl http://127.0.0.1:8001/heroes/999
```

**Test CORS:**
Frontend applications from allowed origins can make requests without CORS errors.
