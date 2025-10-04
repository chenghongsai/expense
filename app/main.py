from fastapi import FastAPI
from sqlalchemy import select
from .db import engine, metadata, SessionLocal
from .orm import map_model_to_tables
from .domain import User
from .security import hash_password
from .config import settings
from .routers import auth, tickets, admin
from fastapi.middleware.cors import CORSMiddleware

# 创建 FastAPI 应用
app = FastAPI(title="Contoso Expense")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup():
    """
    启动钩子：
    1) 建立 ORM 映射（Classical Mapping）
    2) 创建数据表（若不存在）
    3) 确保有一个默认的雇主账号（便于初次启动即可操作）
    """
    # 1) 先完成模型与数据表的映射
    map_model_to_tables()

    # 2) 建表（不存在则创建）
    async with engine.begin() as conn:
        await conn.run_sync(metadata.create_all)

    # 3) 种子默认雇主
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

# 挂载路由分组
app.include_router(auth.router)
app.include_router(tickets.router)
app.include_router(admin.router)
