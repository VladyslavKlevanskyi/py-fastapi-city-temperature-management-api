from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "City Temperature Management API"

    ASYNC_DATABASE_URL: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
