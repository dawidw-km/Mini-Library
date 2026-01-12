from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = True
    PROJECT_NAME: str = "FastAPI Library"
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
    )

settings = Settings() # type: ignore