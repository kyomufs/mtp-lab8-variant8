"""Mini microservice built with FastAPI (advanced task #1).

Routes:
    ``GET /health``       — service health check;
    ``GET /items``        — list stored items;
    ``POST /items``       — store a new item (HTTP 201);
    ``GET /items/{id}``   — one item, HTTP 404 when missing.

Items live in an in-memory dict; ``reset_items`` clears it so
tests stay independent from each other.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="lab8 mini microservice", version="1.0.0")


class Item(BaseModel):
    """Payload accepted by ``POST /items``."""

    name: str = Field(description="item name")
    price: float = Field(description="non-negative price", ge=0)
    in_stock: bool = True


class ItemOut(Item):
    """Stored item together with its assigned identifier."""

    id: int


_items: dict[int, Item] = {}
_next_id: int = 1


def reset_items() -> None:
    """Drop all stored items and reset the id counter.

    Tests call it before each case to isolate them.
    """
    global _next_id
    _items.clear()
    _next_id = 1


@app.get("/health")
def health() -> dict[str, str]:
    """Return the service health status."""
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemOut])
def list_items() -> list[ItemOut]:
    """Return every stored item ordered by identifier."""
    return [
        ItemOut(id=item_id, **item.model_dump())
        for item_id, item in sorted(_items.items())
    ]


@app.post("/items", response_model=ItemOut, status_code=201)
def create_item(item: Item) -> ItemOut:
    """Store ``item`` under a fresh identifier and return it."""
    global _next_id
    item_id = _next_id
    _next_id += 1
    _items[item_id] = item
    return ItemOut(id=item_id, **item.model_dump())


@app.get("/items/{item_id}", response_model=ItemOut)
def get_item(item_id: int) -> ItemOut:
    """Return one stored item.

    Raises:
        HTTPException: with status 404 when ``item_id`` is
        unknown.
    """
    if item_id not in _items:
        raise HTTPException(status_code=404, detail="item not found")
    return ItemOut(id=item_id, **_items[item_id].model_dump())
