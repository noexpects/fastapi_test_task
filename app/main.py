from .routers import users
from fastapi import FastAPI
from .database.create_db import create_db

create_db()
app = FastAPI()
app.include_router(users.router)

