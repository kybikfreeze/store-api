from fastapi import FastAPI, HTTPException

app = FastAPI()

# простая "база в памяти"
items = []


# -------------------------
# CREATE
# -------------------------
@app.post("/items")
def create_item(item: dict):
    items.append(item)
    return {
        "message": "created",
        "item": item,
        "id": len(items) - 1
    }


# -------------------------
# READ ALL
# -------------------------
@app.get("/items")
def get_items():
    return {
        "count": len(items),
        "items": items
    }


# -------------------------
# READ BY ID
# -------------------------
@app.get("/items/{item_id}")
def get_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "id": item_id,
        "item": items[item_id]
    }


# -------------------------
# DELETE
# -------------------------
@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")

    removed = items.pop(item_id)
    return {
        "message": "deleted",
        "removed": removed
    }