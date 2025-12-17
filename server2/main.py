from fastapi import FastAPI
from pydantic import BaseModel
import json
from pathlib import Path
import uvicorn

app = FastAPI(title="Items API", version="1.0.0")

DB_PATH = Path("db/shopping_list.json")


class Item(BaseModel):
    name: str
    quantity: int


def check_database_exists(db_path: Path) -> None:
    if not db_path.exists():
        with open(DB_PATH, "w") as f:
            json.dump([], f)


def load_database() -> list[dict]:
    """Load data from JSON file and return as dictionary"""
    try:
        with open(DB_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise ValueError("Database file is not valid JSON.")


def save_database(data: list[dict]) -> None:
    """Save dictionary data to JSON file"""
    with open(DB_PATH, "w") as f:
        json.dump(data, f)


@app.on_event("startup")
async def startup_event():
    check_database_exists(DB_PATH)


@app.get("/items")
async def list_items():
    return load_database()


@app.post("/items/")
async def create_item(item: Item):
    items = load_database()
    ids = [int(k["id"]) for k in items]
    new_id = str(max(ids) + 1) if ids else "1"
    item_dict = {"id": new_id}
    item_dict.update(item.dict())
    items.append(item_dict)

    save_database(items)
    return {
        "message": "Item created successfully",
        "item": {
            "id": item_dict["id"],
            "name": item_dict["name"],
            "quantity": item_dict["quantity"]
        }
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)
