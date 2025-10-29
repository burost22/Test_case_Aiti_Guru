from sqlalchemy import (
    TIMESTAMP,
    Column,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)

from .db import Base


class Product(Base):
    tablename = "products"
    product_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    quantity = Column(Integer, nullable=False, default=0)


class Order(Base):
    tablename = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(255), nullable=True)
    status = Column(String(64), nullable=False, default="new")
    order_date = Column(TIMESTAMP(timezone=True), server_default=func.now())


class OrderItem(Base):
    tablename = "order_items"
    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer, ForeignKey("orders.order_id", ondelete="CASCADE"), nullable=False
    )
    product_id = Column(
        Integer, ForeignKey("products.product_id", ondelete="RESTRICT"), nullable=False
    )
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)

    table_args = (UniqueConstraint("order_id", "product_id", name="uq_order_product"),)
