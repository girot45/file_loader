from datetime import datetime, timedelta

import jwt
import requests
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.config import config
from src.db.db_main import get_db, get_redis
from src.models.user_model import User

router = APIRouter()


async def create_jwt(user_id: int):
    expire = datetime.now(datetime.timezone.utc) + timedelta(
        minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return jwt.encode(
        {"sub": user_id, "exp": expire}, config.JWT_SECRET, algorithm="HS256"
    )


@router.post("/login")
async def login(
    code: str, db: AsyncSession = Depends(get_db), redis=Depends(get_redis)
):
    # Обмен кода на токен Яндекса
    token_url = "https://oauth.yandex.ru/token"
    response = requests.post(
        token_url,
        data={
            "grant_type": "authorization_code",
            "code": code,
            "client_id": config.YANDEX_CLIENT_ID,
            "client_secret": config.YANDEX_CLIENT_SECRET,
        },
    )

    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Ошибка авторизации")

    data = response.json()
    yandex_token = data["access_token"]

    # Получение инфо о пользователе
    user_info = requests.get(
        "https://login.yandex.ru/info",
        headers={"Authorization": f"OAuth {yandex_token}"},
    ).json()

    # Проверка в БД
    result = await db.execute(
        User.__table__.select().where(User.ya_id == user_info["id"])
    )
    user = result.fetchone()

    if not user:
        user = User(ya_id=user_info["id"], email=user_info["default_email"])
        db.add(user)
        await db.commit()

    # Генерация токенов
    access_token = await create_jwt(user.id)
    refresh_token = f"refresh-{user.id}"

    # Храним refresh_token в Redis
    await redis.setex(refresh_token, config.REFRESH_TOKEN_EXPIRE_DAYS * 86400, "valid")

    return {"access_token": access_token, "refresh_token": refresh_token}


@router.post("/refresh")
async def refresh(refresh_token: str, redis=Depends(get_redis)):
    valid = await redis.get(refresh_token)
    if not valid:
        raise HTTPException(status_code=401, detail="Недействительный токен")

    user_id = int(refresh_token.split("-")[1])
    access_token = await create_jwt(user_id)

    return {"access_token": access_token}
