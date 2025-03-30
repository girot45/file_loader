from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
)
from src.db.db_main import intpk


class Base(DeclarativeBase):
    id: Mapped[intpk]
