from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas, models
from app.database import get_db_session
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.Restaurant)
async def create_restaurant(restaurant: schemas.RestaurantCreate, db: AsyncSession = Depends(get_db_session)):
    db_restaurant = models.Restaurant(name=restaurant.name, capacity=restaurant.capacity, rating=restaurant.rating)
    return await crud.create_restaurant(db, db_restaurant)

@router.post("/menu", response_model=schemas.MenuItem)
async def create_menu_item(menu_item: schemas.MenuItemCreate, db: AsyncSession = Depends(get_db_session)):
    # Check if the restaurant exists
    restaurant = await crud.get_restaurant(db, menu_item.restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    
    db_menu_item = models.MenuItem(name=menu_item.name, price=menu_item.price, restaurant_id=menu_item.restaurant_id)
    return await crud.create_menu_item(db, db_menu_item)


@router.put("/menu/{menu_item_id}", response_model=schemas.MenuItem)
async def update_menu_item(menu_item_id: int, menu_item: schemas.MenuItemCreate, db: AsyncSession = Depends(get_db_session)):
    db_menu_item = await crud.get_menu_item(db, menu_item_id)
    if not db_menu_item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    db_menu_item.name = menu_item.name
    db_menu_item.price = menu_item.price
    db_menu_item.restaurant_id = menu_item.restaurant_id
    
    return await crud.update_menu_item(db, db_menu_item)

@router.get("/menu-items", response_model=List[schemas.MenuItem])
async def list_all_menu_items(db: AsyncSession = Depends(get_db_session)):
    return await crud.get_all_menu_items(db)

@router.get("/", response_model=List[schemas.Restaurant])
async def list_all_restaurants(db: AsyncSession = Depends(get_db_session)):
    return await crud.get_all_restaurants(db)