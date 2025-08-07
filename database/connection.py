import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from .models import Base

# 数据库配置
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://aug_user:aug_password@localhost:5432/aug_db"
)
ASYNC_DATABASE_URL = os.getenv(
    "ASYNC_DATABASE_URL",
    "postgresql+asyncpg://aug_user:aug_password@localhost:5432/aug_db"
)

# 同步引擎和会话
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 异步引擎和会话
async_engine = create_async_engine(ASYNC_DATABASE_URL)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)

def create_tables():
    """创建数据库表"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """获取数据库会话（同步）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """获取数据库会话（异步）"""
    async with AsyncSessionLocal() as session:
        yield session 