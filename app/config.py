from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_env: str = "dev"
    database_url: str

settings = Settings()
