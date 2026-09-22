from fastapi import FastAPI
from pydantic import BaseModel
from datetime import date, datetime

app = FastAPI()


class Item(BaseModel):
    name: str
    price: float
    is_offer: bool | None = None

class User(BaseModel):
    id: int 
    name: str = "John Doe"
    signup_ts: datetime | None = None
    friends: list[int] = []

external_data = {
    "id":"101",
    "signup_ts":"2018-06-01 12:22",
    "friends":[1,"2",b"3"],
}

user = User(**external_data)
print(user)
print(user.id)
@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id}
from typing import Annotated
def say_hello(name: Annotated[str, "this is just metadata"]) -> str:
    return f"Hello {name}"


