from pydantic import BaseModel
from typing import List, Optional

class RestaurantBase(BaseModel):
    name: str
    capacity: int
    rating: int

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int

    class Config:
        orm_mode = True

class MenuItemBase(BaseModel):
    name: str
    price: float

class MenuItemCreate(MenuItemBase):
    restaurant_id: int

class MenuItem(MenuItemBase):
    id: int
    restaurant_id: int

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    item_name: str
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    menu_item_id: int

    class Config:
        orm_mode = True

class OrderBase(BaseModel):
    customer_name: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class Order(OrderBase):
    id: int
    restaurant_id: int
    is_dispatched: bool
    items: List[OrderItem]

    class Config:
        orm_mode = True