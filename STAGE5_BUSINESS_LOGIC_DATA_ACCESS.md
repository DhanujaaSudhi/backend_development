# Stage 5: Business Logic and Data Access

## Acceptance Criteria

✅ **Route functions are short and readable** - Routes delegate to service layer
✅ **Business logic lives in separate files** - Service layer contains business logic
✅ **Database queries in separate files** - Repository layer handles data access
✅ **Thin routes** - Routes only handle HTTP concerns and delegate

## Architecture

### Layered Architecture
```
┌─────────────────────────────────────┐
│         Routes (main.py)            │  HTTP handling, validation
├─────────────────────────────────────┤
│      Services (service.py)          │  Business logic, orchestration
├─────────────────────────────────────┤
│    Repositories (repository.py)     │  Data access, CRUD operations
├─────────────────────────────────────┤
│       Models (models.py)            │  Data models, validation
└─────────────────────────────────────┘
```

### Responsibilities

**Routes (main.py):**
- Handle HTTP requests/responses
- Validate input via Pydantic
- Delegate to service layer
- Convert service errors to HTTP errors
- Return formatted responses

**Services (service.py):**
- Implement business logic
- Orchestrate repository calls
- Apply business rules (e.g., password validation, tax calculation)
- Handle domain-specific errors

**Repositories (repository.py):**
- Handle data access operations
- CRUD operations (Create, Read, Update, Delete)
- Data transformation
- Storage abstraction (in-memory, database, etc.)

**Models (models.py):**
- Define data structures
- Pydantic validation
- Response envelopes
- Domain models

## Implementation

### Before (Monolithic)
```python
@app.post("/api/v1/items/")
async def create_item(item: ItemCreate) -> SuccessResponse:
    # Business logic mixed with route
    item_dict = item.model_dump()
    item_dict["id"] = 1
    if item.tax is not None:
        price_with_tax = item.price + item.tax
        item_dict["price_with_tax"] = price_with_tax
    return SuccessResponse(data=ItemResponse(**item_dict))
```

### After (Layered)
**Route (main.py):**
```python
@app.post("/api/v1/items/")
async def create_item(item: ItemCreate) -> SuccessResponse:
    """Create a new item with automatic tax calculation."""
    try:
        result = ItemService.create_item(item)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Service (service.py):**
```python
class ItemService:
    @staticmethod
    def create_item(item: ItemCreate) -> ItemResponse:
        """Create a new item with automatic tax calculation"""
        # Business logic: Calculate price with tax
        item_dict = item.model_dump()
        if item.tax is not None:
            item_dict["price_with_tax"] = item.price + item.tax
        
        # Delegate to repository
        return ItemRepository.create(ItemCreate(**item_dict))
```

**Repository (repository.py):**
```python
class ItemRepository:
    @classmethod
    def create(cls, item: ItemCreate) -> ItemResponse:
        """Create a new item"""
        item_dict = item.model_dump()
        item_id = cls._next_id
        cls._next_id += 1
        item_dict["id"] = item_id
        cls._items_db[item_id] = item_dict
        return ItemResponse(**item_dict)
```

## Benefits

### Separation of Concerns
- Each layer has a single responsibility
- Easy to understand and maintain
- Changes in one layer don't affect others

### Testability
- Services can be tested independently
- Repositories can be mocked for testing
- Routes only test HTTP handling

### Reusability
- Services can be called from multiple routes
- Repositories can be reused across services
- Business logic centralized

### Scalability
- Easy to add new data sources (swap repository implementation)
- Easy to add business rules (modify service layer)
- Easy to add new endpoints (add new routes using existing services)

### Maintainability
- Clear file structure
- Easy to locate code
- Reduced code duplication

## File Structure

```
d:\work\8stages\
├── app/
│   ├── __init__.py
│   ├── models.py          # Data models and validation
│   ├── repository.py      # Data access layer
│   └── service.py         # Business logic layer
├── main.py                # Routes (thin)
├── pyproject.toml
└── README.md
```

## Key Patterns

### Service Layer Pattern
- Encapsulates business logic
- Coordinates repository operations
- Implements business rules
- Handles domain errors

### Repository Pattern
- Abstracts data access
- Provides CRUD operations
- Hides storage implementation
- Enables easy testing

### Dependency Injection
- Services depend on repositories
- Routes depend on services
- Easy to swap implementations
- Facilitates testing

## Example: Complete Flow

### Request Flow
```
HTTP Request
    ↓
Route (main.py)
    - Validates input
    - Calls service
    ↓
Service (service.py)
    - Applies business logic
    - Calls repository
    ↓
Repository (repository.py)
    - Accesses data
    - Returns result
    ↓
Service (service.py)
    - Processes result
    - Returns to route
    ↓
Route (main.py)
    - Formats response
    - Returns HTTP response
```

### Code Example: Create User

**Route:**
```python
@app.post("/api/v1/users/")
async def create_user(user: UserIn) -> SuccessResponse:
    try:
        result = UserService.create_user(user)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

**Service:**
```python
@staticmethod
def create_user(user: UserIn) -> UserOut:
    # Business logic: Validate password strength
    if len(user.password) < 8:
        raise ValueError("Password must be at least 8 characters long")
    
    # Delegate to repository
    return UserRepository.create(user)
```

**Repository:**
```python
@classmethod
def create(cls, user: UserIn) -> UserOut:
    user_dict = user.model_dump()
    user_id = cls._next_id
    cls._next_id += 1
    user_dict["id"] = user_id
    cls._users_db[user_id] = user_dict
    user_dict.pop("password", None)
    return UserOut(**user_dict)
```

## Migration Notes

### What Changed
- Moved models from main.py to app/models.py
- Created app/repository.py for data access
- Created app/service.py for business logic
- Refactored main.py to use service layer
- Routes now delegate to services

### What Stayed the Same
- API endpoints unchanged
- Request/response formats unchanged
- Validation logic unchanged
- Business logic unchanged (just moved)

### Testing Strategy
- Test services independently (no HTTP)
- Test repositories independently (no business logic)
- Test routes with mocked services
- Integration tests for full flow

## Next Steps

1. **Add Database Integration**: Replace in-memory storage with SQLModel/SQLAlchemy
2. **Add Authentication**: Implement JWT authentication in service layer
3. **Add Logging**: Add logging to service layer for debugging
4. **Add Caching**: Add caching in repository layer for performance
5. **Add Tests**: Write unit tests for services and repositories
