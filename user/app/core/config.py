from pydantic import BaseSettings
import os


class Settings(BaseSettings):
    AWS_USER_TABLE_NAME: str = os.getenv("AWS_USER_TABLE_NAME")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM")
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    )


settings = Settings()
