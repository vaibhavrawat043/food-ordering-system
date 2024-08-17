from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from app.models import Restaurant, MenuItem, Order, OrderItem
from app.schemas import OrderCreate, MenuItemCreate
from sqlalchemy.future import select
from fastapi import HTTPException

async def create_restaurant(db: AsyncSession, restaurant: Restaurant) -> Restaurant:
    async with db.begin():
        db.add(restaurant)
        await db.flush()
        await db.refresh(restaurant)
    return restaurant

async def get_restaurant(db: AsyncSession, restaurant_id: int):
    async with db.begin():
        result = await db.execute(select(Restaurant).filter(Restaurant.id == restaurant_id))
    return result.scalar()

async def create_menu_item(db: AsyncSession, menu_item: MenuItemCreate) -> MenuItem:
    # Check if the restaurant exists
    restaurant = await get_restaurant(db, menu_item.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    async with db.begin():
        db_menu_item = MenuItem(name=menu_item.name, price=menu_item.price, restaurant_id=menu_item.restaurant_id)
        db.add(db_menu_item)
        await db.commit()
        await db.refresh(db_menu_item)
    return db_menu_item

async def get_all_restaurants(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Restaurant))
    return result.scalars().all()

async def get_menu_items_for_restaurant(db: AsyncSession, restaurant_id: int):
    async with db.begin():
        result = await db.execute(select(MenuItem).filter(MenuItem.restaurant_id == restaurant_id))
    return result.scalars().all()


async def get_menu_item_by_name_and_restaurant(db: AsyncSession, item_name: str, restaurant_id: int) -> MenuItem:
    result = await db.execute(
        select(MenuItem).filter(MenuItem.name == item_name, MenuItem.restaurant_id == restaurant_id)
    )
    return result.scalar_one_or_none()

async def update_restaurant_capacity(db: AsyncSession, restaurant_id: int, capacity_change: int) -> Restaurant:
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        return None
    restaurant.capacity += capacity_change
    await db.commit()
    return restaurant


async def dispatch_order(db: AsyncSession, order_id: int) -> Order:
    order = await db.get(Order, order_id)
    if not order:
        return None
    order.is_dispatched = True
    await db.commit()
    await db.refresh(order)
    return order

async def get_order_total_quantity(db: AsyncSession, order_id: int) -> int:
    result = await db.execute(
        select(func.sum(OrderItem.quantity)).filter(OrderItem.order_id == order_id)
    )
    return result.scalar_one_or_none() or 0

async def update_restauraant_capacity_after_dispatch(db: AsyncSession, restaurant_id: int, order_id: int) -> Restaurant:
    quantity = await get_order_total_quantity(db, order_id)
    restaurant = await db.get(Restaurant, restaurant_id)
    if not restaurant:
        return None
    restaurant.capacity += quantity
    await db.commit()
    await db.refresh(restaurant)
    return restaurant

async def get_all_menu_items(db: AsyncSession):
    result = await db.execute(select(MenuItem))
    return result.scalars().all()

async def get_order(db: AsyncSession, order_id: int):
    result = await db.execute(select(Order).filter(Order.id == order_id))
    return result.scalar_one_or_none()