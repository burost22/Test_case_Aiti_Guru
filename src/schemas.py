from pydantic import BaseModel, Field


class AddItemRequest(BaseModel):
    product_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0)


class OrderItemResponse(BaseModel):
    order_item_id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: float
