# Stage 5: Business Logic & Data Access

## Acceptance Criteria

✅ **Business rules in a service layer, not the route** - Service layer contains business logic
✅ **DB queries in a repository layer** - Repository layer handles data access
✅ **Routes are thin** - Routes delegate to service layer (3-5 lines)
✅ **Relevant business rules enforced** - Password validation, tax calculation, sorting

## Architecture

### Layered Structure
```
Routes (main.py) → Services (service.py) → Repositories (repository.py) → Models (models.py)
```

### Responsibilities
- **Routes**: HTTP handling, validation, error conversion
- **Services**: Business logic, orchestration, business rules
- **Repositories**: Data access, CRUD operations
- **Models**: Data structures, validation

## Implementation

### Route (Thin)
```python
@app.post("/api/v1/items/")
async def create_item(item: ItemCreate) -> SuccessResponse:
    try:
        result = ItemService.create_item(item)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
```

### Service (Business Logic)
```python
class ItemService:
    @staticmethod
    def create_item(item: ItemCreate) -> ItemResponse:
        # Business logic: Calculate price with tax
        item_dict = item.model_dump()
        if item.tax is not None:
            item_dict["price_with_tax"] = item.price + item.tax
        return ItemRepository.create(ItemCreate(**item_dict))
```

### Repository (Data Access)
```python
class ItemRepository:
    @classmethod
    def create(cls, item: ItemCreate) -> ItemResponse:
        item_dict = item.model_dump()
        item_dict["id"] = cls._next_id
        cls._next_id += 1
        cls._items_db[item_dict["id"]] = item_dict
        return ItemResponse(**item_dict)
```

## Business Rules Enforced

- **Tax Calculation**: Automatic price_with_tax calculation in service layer
- **Password Validation**: Minimum 8 characters enforced in service layer
- **Sorting**: Applied in service layer based on query parameters
- **Data Security**: Password removed in repository layer before returning

## File Structure
```
app/
├── models.py       # Data models
├── repository.py   # Data access
└── service.py      # Business logic
main.py             # Routes (thin)
```

## Benefits
- **Separation of Concerns**: Each layer has single responsibility
- **Testability**: Services and repositories can be tested independently
- **Reusability**: Services can be called from multiple routes
- **Maintainability**: Easy to locate and modify code
