from typing import Optional

from app.models import ErrorCode, ErrorDetail, ItemCreate, ItemResponse, SortOrder, UserIn, UserOut
from app.repository import ItemRepository, UserRepository


class ItemService:
    """Service layer for item business logic"""
    
    @staticmethod
    def create_item(item: ItemCreate) -> ItemResponse:
        """Create a new item with automatic tax calculation"""
        # Business logic: Calculate price with tax
        item_dict = item.model_dump()
        if item.tax is not None:
            item_dict["price_with_tax"] = item.price + item.tax
        
        # Delegate to repository
        return ItemRepository.create(ItemCreate(**item_dict))
    
    @staticmethod
    def get_item(item_id: int) -> ItemResponse:
        """Get an item by ID"""
        item = ItemRepository.get_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        return item
    
    @staticmethod
    def list_items(
        offset: int = 0,
        limit: int = 100,
        sort_by: str = "id",
        order: SortOrder = SortOrder.asc
    ) -> list[ItemResponse]:
        """List items with pagination and sorting"""
        items = ItemRepository.list_all(offset, limit)
        
        # Business logic: Apply sorting
        if sort_by in ["id", "name", "price"]:
            reverse = order == SortOrder.desc
            items.sort(key=lambda x: getattr(x, sort_by), reverse=reverse)
        
        return items
    
    @staticmethod
    def update_item(item_id: int, item_data: dict) -> ItemResponse:
        """Update an item"""
        # Business logic: Recalculate price with tax if tax changed
        if "tax" in item_data or "price" in item_data:
            existing_item = ItemRepository.get_by_id(item_id)
            if existing_item:
                price = item_data.get("price", existing_item.price)
                tax = item_data.get("tax", existing_item.tax)
                if tax is not None:
                    item_data["price_with_tax"] = price + tax
        
        # Delegate to repository
        updated_item = ItemRepository.update(item_id, item_data)
        if not updated_item:
            raise ValueError(f"Item with id {item_id} not found")
        return updated_item
    
    @staticmethod
    def delete_item(item_id: int) -> bool:
        """Delete an item"""
        item = ItemRepository.get_by_id(item_id)
        if not item:
            raise ValueError(f"Item with id {item_id} not found")
        return ItemRepository.delete(item_id)


class UserService:
    """Service layer for user business logic"""
    
    @staticmethod
    def create_user(user: UserIn) -> UserOut:
        """Create a new user"""
        # Business logic: Validate password strength
        if len(user.password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Delegate to repository
        return UserRepository.create(user)
    
    @staticmethod
    def get_user(user_id: int) -> UserOut:
        """Get a user by ID"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return user
    
    @staticmethod
    def list_users(offset: int = 0, limit: int = 100) -> list[UserOut]:
        """List users with pagination"""
        return UserRepository.list_all(offset, limit)
    
    @staticmethod
    def update_user(user_id: int, user_data: dict) -> UserOut:
        """Update a user"""
        # Business logic: Validate password if being updated
        if "password" in user_data and len(user_data["password"]) < 8:
            raise ValueError("Password must be at least 8 characters long")
        
        # Delegate to repository
        updated_user = UserRepository.update(user_id, user_data)
        if not updated_user:
            raise ValueError(f"User with id {user_id} not found")
        return updated_user
    
    @staticmethod
    def delete_user(user_id: int) -> bool:
        """Delete a user"""
        user = UserRepository.get_by_id(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} not found")
        return UserRepository.delete(user_id)
