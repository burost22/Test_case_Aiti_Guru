import asyncio

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from . import models, schemas

MAX_RETRIES = 3
RETRY_BACKOFF = 0.05  # seconds


async def add_item_to_order(
    db: AsyncSession, order_id: int, item: schemas.AddItemRequest
):
    """
    Добавляет товар в заказ без логики со складом:
    - проверяет существование заказа и его статус
    - если order_item уже есть -> увеличивает quantity (блокируя row через FOR UPDATE)
    - иначе создаёт новую позицию (берёт unit_price из products) — при этом НЕ меняет products.quantity
    - защищено от race через попытки при IntegrityError
    """
    # Проверяем существование заказа
    order = await db.get(models.Order, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    if order.status and order.status.lower() in ("cancelled", "completed", "shipped"):
        raise HTTPException(
            status_code=400,
            detail=f"Order status '{order.status}' does not allow modifications",
        )

    attempt = 0
    while True:
        attempt += 1
        try:
            async with db.begin():
                # Пытаемся найти существующую позицию заказа и заблокировать её для обновления
                oi_stmt = (
                    select(models.OrderItem)
                    .where(
                        models.OrderItem.order_id == order_id,
                        models.OrderItem.product_id == item.product_id,
                    )
                    .with_for_update()
                )
                res = await db.execute(oi_stmt)
                order_item = res.scalar_one_or_none()

                if order_item:
                    # Если позиция уже есть — увеличиваем quantity
                    order_item.quantity = order_item.quantity + item.quantity
                    db.add(order_item)
                    await db.flush()
                    return order_item

                # Позиции нет — проверим, существует ли сам товар (чтобы взять unit_price)
                product = await db.get(models.Product, item.product_id)
                if product is None:
                    raise HTTPException(
                        status_code=404, detail=f"Product {item.product_id} not found"
                    )

                # Создаём новую позицию (НЕ трогаем product.quantity)
                new_item = models.OrderItem(
                    order_id=order_id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=product.price,
                )
                db.add(new_item)
                await db.flush()  # может выбросить IntegrityError при конкурентной вставке
                return new_item

        except IntegrityError as exc:
            # Конкурентный INSERT мог создать запись после нашей проверки — сделаем retry
            await db.rollback()
            if attempt >= MAX_RETRIES:
                raise HTTPException(
                    status_code=500,
                    detail="Could not add item due to concurrent updates; please retry",
                ) from exc
            # небольшой backoff и повтор
            await asyncio.sleep(RETRY_BACKOFF * attempt)
            continue
