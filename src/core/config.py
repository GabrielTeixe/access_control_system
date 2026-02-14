from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str ="123456"
    ALGORITHM: str ="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    class Config:
        env_file =".env"

settings = Settings()