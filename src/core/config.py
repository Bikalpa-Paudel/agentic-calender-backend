from pydantic_settings import BaseSettings

class Setting(BaseSettings):
    DB_URL : str

    class Config:
        env_file = ".env"


settings = Setting()
