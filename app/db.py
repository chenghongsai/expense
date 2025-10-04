from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import registry
from .config import settings

# 注册表映射（Classical Mapping 用这个）
mapper_registry = registry()
metadata = mapper_registry.metadata

# 创建异步数据库引擎
engine = create_async_engine(settings.db_url, echo=False, future=True)

# 创建异步会话工厂
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
