import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..models import models
from ..main import app
from ..routers.users import get_db


@pytest.fixture(scope="session")
def test_db():
    engine = create_engine("postgresql://postgres:12345@db",
                           echo=True
                           )

    with engine.connect() as connection:
        connection.execute("commit")
        connection.execute("DROP DATABASE IF EXISTS test_fastapi")
        connection.execute("commit")
        connection.execute("CREATE DATABASE test_fastapi")

    engine = create_engine("postgresql://postgres:12345@db/test_fastapi",
                           echo=True
                           )

    testsessionlocal = sessionmaker(bind=engine)

    models.Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = testsessionlocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    yield
