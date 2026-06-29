from datetime import datetime, timezone
from typing import Optional

from app.models import ItemCreate, ItemResponse, UserIn, UserOut


class ItemRepository:
    """Repository for item data access operations"""
    
    # In-memory storage (replace with database in production)
    _items_db: dict[int, dict] = {}
    _next_id: int = 1
    
    @classmethod
    def create(cls, item: ItemCreate) -> ItemResponse:
        """Create a new item"""
        item_dict = item.model_dump()
        item_id = cls._next_id
        cls._next_id += 1
        item_dict["id"] = item_id
        item_dict["created_at"] = datetime.now(timezone.utc)
        
        cls._items_db[item_id] = item_dict
        return ItemResponse(**item_dict)
    
    @classmethod
    def get_by_id(cls, item_id: int) -> Optional[ItemResponse]:
        """Get an item by ID"""
        item_data = cls._items_db.get(item_id)
        if item_data:
            return ItemResponse(**item_data)
        return None
    
    @classmethod
    def list_all(cls, offset: int = 0, limit: int = 100) -> list[ItemResponse]:
        """List all items with pagination"""
        items = list(cls._items_db.values())
        paginated_items = items[offset:offset + limit]
        return [ItemResponse(**item) for item in paginated_items]
    
    @classmethod
    def update(cls, item_id: int, item_data: dict) -> Optional[ItemResponse]:
        """Update an item"""
        if item_id not in cls._items_db:
            return None
        
        cls._items_db[item_id].update(item_data)
        return ItemResponse(**cls._items_db[item_id])
    
    @classmethod
    def delete(cls, item_id: int) -> bool:
        """Delete an item"""
        if item_id in cls._items_db:
            del cls._items_db[item_id]
            return True
        return False


class UserRepository:
    """Repository for user data access operations"""
    
    # In-memory storage (replace with database in production)
    _users_db: dict[int, dict] = {}
    _next_id: int = 1
    
    @classmethod
    def create(cls, user: UserIn) -> UserOut:
        """Create a new user"""
        user_dict = user.model_dump()
        user_id = cls._next_id
        cls._next_id += 1
        user_dict["id"] = user_id
        user_dict["created_at"] = datetime.now(timezone.utc)
        
        cls._users_db[user_id] = user_dict
        # Remove password before returning
        user_dict.pop("password", None)
        return UserOut(**user_dict)
    
    @classmethod
    def get_by_id(cls, user_id: int) -> Optional[UserOut]:
        """Get a user by ID"""
        user_data = cls._users_db.get(user_id)
        if user_data:
            # Remove password before returning
            user_data_copy = user_data.copy()
            user_data_copy.pop("password", None)
            return UserOut(**user_data_copy)
        return None
    
    @classmethod
    def list_all(cls, offset: int = 0, limit: int = 100) -> list[UserOut]:
        """List all users with pagination"""
        users = list(cls._users_db.values())
        paginated_users = users[offset:offset + limit]
        result = []
        for user in paginated_users:
            user_copy = user.copy()
            user_copy.pop("password", None)
            result.append(UserOut(**user_copy))
        return result
    
    @classmethod
    def update(cls, user_id: int, user_data: dict) -> Optional[UserOut]:
        """Update a user"""
        if user_id not in cls._users_db:
            return None
        
        cls._users_db[user_id].update(user_data)
        user_data_copy = cls._users_db[user_id].copy()
        user_data_copy.pop("password", None)
        return UserOut(**user_data_copy)
    
    @classmethod
    def delete(cls, user_id: int) -> bool:
        """Delete a user"""
        if user_id in cls._users_db:
            del cls._users_db[user_id]
            return True
        return False
