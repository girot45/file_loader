from fastapi import FastAPI
from src.api.auth import router as auth_router
from src.api.users import router as users_router
# from files import router as files_router

app = FastAPI()

# app.include_router(users_router, tags=["Users"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
# app.include_router(files_router, prefix="/files", tags=["Files"])
