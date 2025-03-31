import os
from functools import lru_cache

from dotenv import load_dotenv
from src.config.config_models import Config, DbConfig

load_dotenv()


@lru_cache(maxsize=None)
def get_config() -> Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY")
    ALGORITHM: str = os.environ.get("ALGORITHM")
    KEY: str = os.environ.get("KEY")
    REDIS_URL: str = os.environ.get("REDIS_URL")
    YANDEX_CLIENT_ID:str = os.environ.get("YANDEX_CLIENT_ID"),
    YANDEX_CLIENT_SECRET:str = os.environ.get("YANDEX_CLIENT_SECRET")
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    db_host: str = os.environ.get("DB_HOST")
    db_name: str = os.environ.get("DB_NAME")
    db_user: str = os.environ.get("DB_USER")
    db_pass: str = os.environ.get("DB_PASS")
    db_port: str = os.environ.get("DB_PORT")

    return Config(
        KEY=KEY,
        SECRET_KEY=SECRET_KEY,
        ALGORITHM=ALGORITHM,
        REDIS_URL=REDIS_URL,
        YANDEX_CLIENT_ID = YANDEX_CLIENT_ID,
        YANDEX_CLIENT_SECRET = YANDEX_CLIENT_SECRET,
        ACCESS_TOKEN_EXPIRE_MINUTES=ACCESS_TOKEN_EXPIRE_MINUTES,
        REFRESH_TOKEN_EXPIRE_DAYS=REFRESH_TOKEN_EXPIRE_DAYS,
        db_config=DbConfig(
            db_host=db_host,
            db_name=db_name,
            db_user=db_user,
            db_pass=db_pass,
            db_port=db_port,
        ),
    )
