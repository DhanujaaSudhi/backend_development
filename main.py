from typing import Annotated
from enum import Enum

from fastapi import Depends, FastAPI, HTTPException, Query
from sqlmodel import Field, Session, SQLModel, create_engine, select

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


# SQLModel Models
class HeroBase(SQLModel):
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)


class Hero(HeroBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    secret_name: str


class HeroPublic(HeroBase):
    id: int


class HeroCreate(HeroBase):
    secret_name: str


class HeroUpdate(HeroBase):
    name: str | None = None
    age: int | None = None
    secret_name: str | None = None


@app.post("/heroes/", response_model=HeroPublic)
def create_hero(hero: HeroCreate, session: SessionDep) -> HeroPublic:
    db_hero = Hero.model_validate(hero)
    session.add(db_hero)
    session.commit()
    session.refresh(db_hero)
    return db_hero


@app.get("/heroes/", response_model=list[HeroPublic])
def read_heroes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
) -> list[HeroPublic]:
    heroes = session.exec(select(Hero).offset(offset).limit(limit)).all()
    return heroes


@app.get("/heroes/{hero_id}", response_model=HeroPublic)
def read_hero(hero_id: int, session: SessionDep) -> HeroPublic:
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero


@app.patch("/heroes/{hero_id}", response_model=HeroPublic)
def update_hero(hero_id: int, hero: HeroUpdate, session: SessionDep) -> HeroPublic:
    hero_db = session.get(Hero, hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    hero_data = hero.model_dump(exclude_unset=True)
    hero_db.sqlmodel_update(hero_data)
    session.add(hero_db)
    session.commit()
    session.refresh(hero_db)
    return hero_db


@app.delete("/heroes/{hero_id}")
def delete_hero(hero_id: int, session: SessionDep):
    hero = session.get(Hero, hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    session.delete(hero)
    session.commit()
    return {"ok": True}


# Stage 4: Query Parameters and Path Parameters Examples

# Query Parameters with Defaults
fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    """
    Query parameters with default values.
    URL example: /items/?skip=0&limit=10
    """
    return fake_items_db[skip : skip + limit]


# Optional Query Parameters
@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    """
    Optional query parameter.
    URL example: /items/foo?q=search
    """
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}


# Boolean Query Parameters
@app.get("/items/{item_id}/detail")
async def read_item_detail(item_id: str, q: str | None = None, short: bool = False):
    """
    Boolean query parameter with automatic conversion.
    URL example: /items/foo/detail?short=true
    """
    item = {"item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Required Query Parameters
@app.get("/items/{item_id}/required")
async def read_user_item(item_id: str, needy: str):
    """
    Required query parameter.
    URL example: /items/foo/required?needy=value
    """
    item = {"item_id": item_id, "needy": needy}
    return item


# Multiple Parameters
@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    """
    Multiple path and query parameters.
    URL example: /users/1/items/foo?q=search&short=true
    """
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {"description": "This is an amazing item that has a long description"}
        )
    return item


# Path Parameters with Types
@app.get("/items/{item_id}/typed")
async def read_item_typed(item_id: int):
    """
    Path parameter with type validation.
    URL example: /items/3/typed
    """
    return {"item_id": item_id}


# Enum for Predefined Values
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    """
    Path parameter with predefined enum values.
    URL example: /models/alexnet
    """
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}

    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}

    return {"model_name": model_name, "message": "Have some residuals"}


# Path Convertor for Paths
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    """
    Path parameter containing a path.
    URL example: /files//home/johndoe/myfile.txt (note double slash)
    """
    return {"file_path": file_path}
