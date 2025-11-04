from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = True
    PROJECT_NAME: str = "FastAPI Library"

    class Config:
        env_file = ".env"

settings = Settings()
