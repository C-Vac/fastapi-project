from pydantic_settings import BaseSettings

SQLALCHEMY_DATABASE_URL = (
    "postgresql+psycopg://fastapi-app:password123@localhost:5432/fastapi"
)


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


settings = Settings(
    database_hostname="localhost",
    database_port="5432",
    database_username="fastapi-app",
    database_password="password123",
    database_name="fastapi",
    secret_key="secret",
    algorithm="HS256",
    access_token_expire_minutes=60,
)
