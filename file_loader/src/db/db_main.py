from typing import Annotated

from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import mapped_column, sessionmaker
from sqlalchemy.schema import Identity

from src.config import config

engine = create_async_engine(config.db_config.get_url())
async_session_maker = sessionmaker(  # noqa
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    
)

intpk = Annotated[int, mapped_column(
    Integer,
    primary_key=True,
    server_default=Identity()
)]
