import jwt
from src.db.db_main import get_db
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.models.user_model import User
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import config

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    try:
        payload = jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(User.__table__.select().where(User.id == user_id))
    user = result.fetchone()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
