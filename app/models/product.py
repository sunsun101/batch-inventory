"""
Product Model
"""
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class Product(SQLModel, table=True):
    """
    Product Model
    """
    __tablename__ = 'products'

    id: int = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float

    batches: List["Batch"] = Relationship(back_populates="product")
