from typing import List

from pydantic import BaseModel


class ItemBase(BaseModel):
    """Pydantic model for the 'items' database table."""

    article_id: str
    embedding: List[float]

    class Config:
        from_attributes = True


class ItemCreate(ItemBase):
    """Pydantic model for creating a new item."""

    pass


class ItemRead(ItemBase):
    """Pydantic model for reading an item, including its ID."""

    id: int
