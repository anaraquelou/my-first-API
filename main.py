from fastapi import FastAPI, HTTPException, Query, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()
    
class Supplier(BaseModel):
    id: int
    is_active: bool = True

class Item(BaseModel):
    name: Annotated[str | None, Query(max_length=50)]
    in_stock: bool = False
    price: float = Field(gt=0, description="The price must be greater than zero")
    supplier: Supplier
    
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Example Item",
                    "in_stock": True,
                    "price": 25.99,
                    "supplier": {
                        "id": 12345,
                        "is_active": True
                    },
                }
            ]
        }
    }

    

items = []

@app.get("/")
def root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item: Item):
    items.append(item)
    return items

@app.get("/items", response_model=list[Item])
def list_items(limit: int = 10):
    return items[0:limit]

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int, item: Item):
    if item_id < len(items):
        item = items[item_id]
        return item
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item, updated_by: Annotated[int, Body()]):
    if item_id < len(items):
        items[item_id] = item
        results = {"item_id": item_id, "item": item, "updated_by": updated_by}
        return results
    else:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")

# Use http://127.0.0.1:8000/docs to see a interactive representation of my API
# Click in /openapi.json to get a json to build the API documentation 