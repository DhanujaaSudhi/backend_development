# Stage 4: Route Registration & Input Validation

## Acceptance Criteria

✅ **Route registered** - All endpoints properly registered with FastAPI
✅ **Payload validated against schema** - Pydantic schemas validate all input data
✅ **Invalid input rejected with 400/422 in the agreed field-level envelope** - Uses Stage 2 error envelope format

## Implementation

### Route Registration
```python
@app.post("/api/v1/items/")
@app.get("/api/v1/items/{item_id}")
@app.get("/api/v1/items/")
@app.post("/api/v1/users/")
@app.get("/api/v1/users/{user_id}")
```

### Pydantic Schema Validation
```python
class ItemCreate(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class UserIn(BaseModel):
    username: str
    password: str
    email: EmailStr
    full_name: str | None = None
```

**Validation Features:**
- Type checking (str, int, float, etc.)
- Required fields validation
- Optional fields with defaults
- Email validation via EmailStr
- Automatic error messages

### Error Handling with Stage 2 Envelope
Invalid input is rejected with 422 status using the agreed error envelope format:

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

### Validation Example
**Request (missing required field):**
```json
{
  "name": "Test Item"
}
```

**Response (422):**
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

## Benefits
- **Security**: Never trust client data, all input validated
- **Consistency**: Standardized error format across all endpoints
- **Developer Experience**: Automatic validation with clear error messages
- **Type Safety**: Pydantic ensures type correctness
