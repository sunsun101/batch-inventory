"""
Defines the schemas
"""
from pydantic import BaseModel
from .product import ProductResponse


class BatchCreate(BaseModel):
    """
    Schema for creating a new batch of products in the inventory
    """
    batch_name: str
    product: str
    quantity: int
    purchase_price: float
    sales_price: float
    warehouse: str


class BatchResponse(BaseModel):
    """
    Schema for representing a batch in the inventory
    """
    id: int
    batch_number: str
    batch_name: str
    product: ProductResponse
    quantity: int
    sales_price: float
    warehouse: str

    class Config:
        orm_mode = True


class BatchUpdate(BaseModel):
    """
    Schema for updating quantity in a batch
    """

    batch_number: str
    quantity: int
