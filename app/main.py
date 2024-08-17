from fastapi import FastAPI
from app.api import restaurants, orders
from app.database import get_db_session, get_sync_db_session
import os

app = FastAPI()

app.include_router(restaurants.router, prefix="/restaurants", tags=["restaurants"])
app.include_router(orders.router, prefix="/orders", tags=["orders"])

# Use synchronous db session for testing
if os.environ.get("TESTING"):
    app.dependency_overrides[get_db_session] = get_sync_db_session

@app.get("/")
def read_root():
    return {"message": "Welcome to the Online Food Ordering System!"}