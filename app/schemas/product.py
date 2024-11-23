from pydantic import BaseModel
from typing import Optional


class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float

    class Config:
        from_attributes = True
