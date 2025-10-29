import asyncio

from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession

from . import crud, models, schemas
from .db import Base, engine, get_async_session

# Демо. Создание таблиц. На проде будет alembic


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


asyncio.get_event_loop().create_task(init_models())

app = FastAPI(title="Order Service (async)", version="1.0")


@app.post("/orders/{order_id}/items", response_model=schemas.OrderItemResponse)
async def add_item(
    order_id: int,
    req: schemas.AddItemRequest,
    db: AsyncSession = Depends(get_async_session),
):
    item = await crud.add_item_to_order(db, order_id, req)
    return schemas.OrderItemResponse(
        order_item_id=item.order_item_id,
        order_id=item.order_id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=float(item.unit_price),
    )
