from src.config.auth_manager import get_current_user
from src.db.db_main import get_db
from fastapi import APIRouter, Depends, HTTPException
from src.models.user_model import User
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

router = APIRouter()

class UserUpdate(BaseModel):
    email: str | None = None

class UserUpdateSuperuser(UserUpdate):
    is_superuser: bool | None = None  


@router.get("/users/me")
async def get_my_info(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "is_superuser": user.is_superuser}


@router.put("/users/me")
async def update_my_info(
    data: UserUpdate,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if data.email:
        user.email = data.email
    await db.commit()
    return {"message": "Profile updated"}


@router.delete("/admin/users/{user_id}")
async def delete_user(
    user_id: int,
    admin: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not admin.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return {"message": "User deleted"}


@router.put("/admin/users/{user_id}")
async def update_user(
    user_id: int,
    data: UserUpdateSuperuser,
    admin: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    if not admin.is_superuser:
        raise HTTPException(status_code=403, detail="Not enough permissions")

    user = await db.execute(select(User).where(User.id == user_id))
    user = user.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if data.email:
        user.email = data.email
    if data.is_superuser is not None:
        user.is_superuser = data.is_superuser

    await db.commit()
    return {"message": "User updated"}
