__all__ = ["config", "async_session_maker", ]
from pathlib import Path

from pydantic import PostgresDsn, SecretStr, PositiveInt
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=".env",
        extra="ignore",
    )
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: PostgresDsn
    BOT_TOKEN: str
    JWT_ACCESS_SECRET_KEY: SecretStr
    JWT_REFRESH_SECRET_KEY: SecretStr
    JWT_ACCESS_ALGORITHM: str
    JWT_ACCESS_ALGORITHM: str
    JWT_ACCESS_EXP: PositiveInt
    JWT_REFRESH_EXP: PositiveInt
    JWT_ACCESS_SECRET_KEY: str


MANAGE_APP_MIGRATIONS = [
    "app",
    "auth",
]


config = Config()

async_engine = create_async_engine(url=config.DATABASE_URL.unicode_string())
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)
