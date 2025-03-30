import asyncio
from datetime import datetime
from functools import wraps
from typing import Optional

from fastapi import Request
from sqlalchemy import insert
from src.db.db_main import async_session_maker
from src.models.service_model import (
    Log,
    RequestLog,
)
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Получаем информацию о запросе
        request_info = {
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_host": request.client.host if request.client else None,
            "timestamp": datetime.now(),
        }
        response = await call_next(request)
        request_info["status_code"] = str(response.status_code)
        asyncio.create_task(self.log_request(request_info))  # noqa
        return response

    async def log_request(self, request_info: dict):
        async with async_session_maker() as session:
            request_info["service"] = "file_reader"

            query = insert(RequestLog).values(**request_info)
            await session.execute(query)
            await session.commit()


def logger(message: Optional[str] = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = datetime.now()
            result = await func(*args, **kwargs)
            execution_time = (datetime.now() - start_time).total_seconds()

            async with async_session_maker() as session:
                log_entry = Log(
                    function_name=func.__name__,
                    execution_time=execution_time,
                    message=message,
                    timestamp=start_time,
                )
                session.add(log_entry)
                await session.commit()

            return result

        return wrapper

    return decorator
