from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import registry
from .config import settings

mapper_registry = registry()
metadata = mapper_registry.metadata

engine = create_async_engine(settings.db_url, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
