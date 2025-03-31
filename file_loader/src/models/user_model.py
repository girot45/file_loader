from sqlalchemy import Boolean, text
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base_model import Base


class User(Base):
    __tablename__ = "users"

    ya_id: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))
