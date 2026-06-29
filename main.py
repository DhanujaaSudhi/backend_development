from fastapi import FastAPI, HTTPException

from app.models import ErrorCode, ErrorDetail, ErrorResponse, ItemCreate, ItemResponse, SortOrder, SuccessResponse, UserIn, UserOut
from app.service import ItemService, UserService

app = FastAPI()


# API v1 Endpoints - Thin routes that delegate to service layer
@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    return SuccessResponse(
        data={"status": "healthy", "service": "8stages-api"}
    )


@app.post("/api/v1/items/")
async def create_item(item: ItemCreate) -> SuccessResponse:
    """Create a new item with automatic tax calculation."""
    try:
        result = ItemService.create_item(item)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/items/{item_id}")
async def read_item(item_id: int) -> SuccessResponse:
    """Retrieve an item by ID."""
    try:
        result = ItemService.get_item(item_id)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/api/v1/items/")
async def list_items(
    offset: int = 0,
    limit: int = 100,
    sort_by: str = "id",
    order: SortOrder = SortOrder.asc
) -> SuccessResponse:
    """List items with pagination and sorting."""
    result = ItemService.list_items(offset, limit, sort_by, order)
    return SuccessResponse(data=result)


@app.post("/api/v1/users/")
async def create_user(user: UserIn) -> SuccessResponse:
    """Create a new user. Password is not returned in the response for security."""
    try:
        result = UserService.create_user(user)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/api/v1/users/{user_id}")
async def read_user(user_id: int) -> SuccessResponse:
    """Retrieve a user by ID."""
    try:
        result = UserService.get_user(user_id)
        return SuccessResponse(data=result)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
