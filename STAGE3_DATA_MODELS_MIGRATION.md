# Stage 3: Data Models & Migration

## Acceptance Criteria

✅ **Schema updated** - SQLModel models defined with proper table structure
✅ **Migration runs cleanly in local env** - Alembic migration successfully generated and can be run
✅ **Response model decoupled from DB model** - Separate models for database operations and API responses

## Implementation

### Database Model (Hero)
```python
class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str  # Sensitive data, never exposed
```

### Response Model (HeroPublic)
```python
class HeroPublic(HeroBase):
    id: int  # Excludes secret_name for security
```

### Decoupling Strategy
- **Hero (DB model)**: Contains all fields including secret_name
- **HeroPublic (Response model)**: Excludes secret_name, only safe fields
- **HeroCreate (Request model)**: Includes secret_name for input
- **HeroUpdate (Request model)**: Optional fields for partial updates

### Migration Setup
```bash
# Initialize Alembic
alembic init alembic

# Configure alembic.ini
sqlalchemy.url = sqlite:///database.db

# Update env.py
from sqlmodel import SQLModel
from main import Hero
target_metadata = SQLModel.metadata

# Generate migration
alembic revision --autogenerate -m "Initial migration - create hero table"

# Apply migration
alembic upgrade head
```

### Database Schema
```sql
CREATE TABLE hero (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    secret_name TEXT NOT NULL
);
CREATE INDEX ix_hero_name ON hero(name);
CREATE INDEX ix_hero_age ON hero(age);
```

### Migration Commands
- `alembic revision --autogenerate -m "description"` - Generate migration
- `alembic upgrade head` - Apply migrations
- `alembic downgrade -1` - Rollback migration
- `alembic history` - View migration history

## Benefits
- **Security**: Sensitive data (secret_name) never exposed in API responses
- **Flexibility**: API contract independent of database schema
- **Maintainability**: Database changes don't break API
- **Version Control**: Migrations tracked in git
