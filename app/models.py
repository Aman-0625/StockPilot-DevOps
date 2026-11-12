
from pydantic import BaseModel, Field, ConfigDict


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    category: str = Field(min_length=2, max_length=50)
    quantity: int = Field(ge=0)
    minimum_stock: int = Field(ge=0)
    price: float = Field(gt=0)


class Product(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    quantity: int
    minimum_stock: int
    price: float


class RestockRequest(BaseModel):
    quantity: int = Field(gt=0)
