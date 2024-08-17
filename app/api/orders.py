from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db_session
from app.strategy.restaurant_selection import LowestCostStrategy
from sqlalchemy.exc import IntegrityError

router = APIRouter()

@router.post("/", response_model=schemas.Order)
async def create_order(order: schemas.OrderCreate, db: AsyncSession = Depends(get_db_session)):
    strategy = LowestCostStrategy()
    
    async with db.begin():
        restaurants = await crud.get_all_restaurants(db)
        suitable_restaurants = []

        for restaurant in restaurants:
            menu_items = await crud.get_menu_items_for_restaurant(db, restaurant.id)
            if all(any(item.name == oi.item_name for item in menu_items) for oi in order.items):
                total_quantity = sum(oi.quantity for oi in order.items)
                if total_quantity <= restaurant.capacity:
                    suitable_restaurants.append(restaurant)

        if not suitable_restaurants:
            raise HTTPException(status_code=404, detail="No suitable restaurant found")

        selected_restaurant = await strategy.select_restaurant(suitable_restaurants)

        db_order = models.Order(customer_name=order.customer_name, restaurant_id=selected_restaurant.id)
        db.add(db_order)
        await db.flush()

        for item in order.items:
            menu_item = await crud.get_menu_item_by_name_and_restaurant(db, item.item_name, selected_restaurant.id)
            if not menu_item:
                raise HTTPException(status_code=404, detail=f"Menu item {item.item_name} not found in the selected restaurant")

            db_order_item = models.OrderItem(order_id=db_order.id, menu_item_id=menu_item.id, quantity=item.quantity)
            db.add(db_order_item)

        selected_restaurant.capacity -= sum(item.quantity for item in order.items)
        await db.commit()

    return db_order
    

@router.post("/{order_id}/dispatch", response_model=schemas.Order)
async def dispatch_order(order_id: int, db: AsyncSession = Depends(get_db_session)):
    async with db.begin():
        order = await crud.get_order(db, order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

        if order.is_dispatched:
            raise HTTPException(status_code=400, detail="Order is already dispatched")

        order.is_dispatched = True
        restaurant = await crud.get_restaurant(db, order.restaurant_id)
        restaurant.capacity += sum(item.quantity for item in order.order_items)

        await db.commit()
        await db.refresh(order)

    return order
