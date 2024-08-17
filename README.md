# Food Ordering System

## Overview
This project is a Food Ordering System built with FastAPI, SQLAlchemy, and Pydantic. It provides a robust backend for managing restaurants, menus, and orders with an extensible architecture for restaurant selection strategies.

## Features
- Restaurant management (CRUD operations)
- Menu item management
- Order placement and dispatching
- Extensible restaurant selection strategy



## Setup and Installation
1. Clone the repository:
   ```
   git clone https://github.com/<username>/food-ordering-system.git
   cd food-ordering-system
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database
   - Update the database URL in `app/core/config.py`

5. Run database migrations:
   ```
   alembic upgrade head
   ```

6. Start the server:
   ```
   uvicorn main:app --reload
   ```

## API Documentation
Once the server is running, you can access the API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing
Run the tests using pytest:
```
pytest
```