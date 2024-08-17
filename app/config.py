from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://root:root@localhost/food_ordering_system"
    TEST_DATABASE_URL: str = DATABASE_URL + "_test"

    class Config:
        env_file = ".env"

settings = Settings()