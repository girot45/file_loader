from datetime import datetime

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from src.models.base_model import Base


class RequestLog(Base):
    __tablename__ = "request_logs"

    method: Mapped[str] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    client_host: Mapped[str] = mapped_column(nullable=False)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
    query_params: Mapped[str] = mapped_column(nullable=False)
    service: Mapped[str] = mapped_column(nullable=True)
    status_code: Mapped[str] = mapped_column(nullable=True)


class Log(Base):
    __tablename__ = "logs"
    function_name: Mapped[str] = mapped_column(nullable=False)
    execution_time: Mapped[float] = mapped_column(nullable=False)
    message: Mapped[str] = mapped_column(nullable=True)
    timestamp: Mapped[datetime] = mapped_column(nullable=False)
