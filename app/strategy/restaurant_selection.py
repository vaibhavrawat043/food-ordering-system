# app/strategy/restaurant_selection.py

from abc import ABC, abstractmethod
from app.models import Restaurant

class RestaurantSelectionStrategy(ABC):
    @abstractmethod
    async def select_restaurant(self, restaurants: list[Restaurant]) -> Restaurant:
        pass

class LowestCostStrategy(RestaurantSelectionStrategy):
    async def select_restaurant(self, restaurants: list[Restaurant]) -> Restaurant:
        return min(restaurants, key=lambda r: sum(item.price for item in r.menu_items))

