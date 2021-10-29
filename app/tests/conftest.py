import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from ..models import models
from ..main import app
from ..routers.users import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from ..config import config

settings = config.get_settings()


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine(f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}",
                           echo=True
                           )

    with engine.connect() as connection:
        connection.execute("commit")
        connection.execute(f"DROP DATABASE IF EXISTS {settings.test_db_name}")
        connection.execute("commit")
        connection.execute(f"CREATE DATABASE {settings.test_db_name}")

    engine = create_engine(f"postgresql://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.test_db_name}",
                           echo=True
                           )

    models.Base.metadata.create_all(bind=engine)

    async_engine = create_async_engine(f"postgresql+asyncpg://{settings.db_user}:{settings.db_pass}@{settings.db_host}/{settings.test_db_name}",
                                       echo=True
                                       )

    testsessionlocal = sessionmaker(bind=async_engine, class_=AsyncSession)

    def override_get_db():
        db = testsessionlocal()
        return db

    app.dependency_overrides[get_db] = override_get_db

    yield
