from fastapi import FastAPI
from sqlalchemy import select
from app.db import engine, metadata, SessionLocal
from app.orm import map_model_to_tables
from app.domain import User
from app.security import hash_password
from app.config import settings
from app.routers import auth, tickets, admin

app = FastAPI(title="Contoso Expense")

@app.on_event("startup")
async def on_startup():
    # 建立映射并建表
    map_model_to_tables()
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    # 首启种子雇主
    async with SessionLocal() as session:
        exists = (await session.execute(
            select(User).where(User.email == settings.default_admin_email)
        )).scalar_one_or_none()
        if not exists:
            admin = User(
                email=settings.default_admin_email,
                password_hash=hash_password(settings.default_admin_password),
                role="EMPLOYER",
            )
            session.add(admin)
            await session.commit()

app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(admin.router)
