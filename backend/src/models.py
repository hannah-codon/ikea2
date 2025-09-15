"""
Data models for the API.

This module defines the Pydantic models used for request and response
validation across the application's API endpoints.
"""

from pydantic import BaseModel


class IkeaEntry(BaseModel):
    """Ikea entry model."""

    pid: str
    image_url: str
    name: str
    price: int
    explanation: str
    eco_score: int

class MaterialsTable(BaseModel):
    """Table model."""

    headers: list[str]
    rows: list[list[str]]
