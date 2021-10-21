from .database import engine
from ..models import models


def create_db():
    models.Base.metadata.create_all(bind=engine)
