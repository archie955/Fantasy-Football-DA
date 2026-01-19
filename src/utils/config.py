from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = ".env"

settings = Settings()