"""
batch.py

Database model
"""
from typing import Optional
from sqlmodel import Field, SQLModel, Relationship


class Batch(SQLModel, table=True):
    """
    Database model Batch

    Args:
        SQLModel (_type_): Base model 
        table (bool, optional): Defaults to True.
    """
    __tablename__ = 'batches'

    id: Optional[int] = Field(default=None, primary_key=True)
    batch_number: str = Field(index=True, unique=True, nullable=False)
    batch_name: str
    quantity: int
    sales_price: float
    warehouse: str
    product_id: int = Field(foreign_key="products.id")
    product: "Product" = Relationship(back_populates="batches")
