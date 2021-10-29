from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import config

settings = config.get_settings()

engine = create_async_engine(f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.db_name}",
                             echo=True
                             )

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, class_=AsyncSession)
