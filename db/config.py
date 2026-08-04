from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    mongo_url: str
    database_name: str

    class Config:
        env_file = ".env"


settings = Settings()