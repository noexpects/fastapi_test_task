from sqlalchemy import select
from app.models import models
from app.schemas import user_schemas
from ..hasher.user_pass_hasher import PassHasher


class CRUD:
    def __init__(self, db):
        self.db = db
        self.hasher = PassHasher()

    async def get_user(self, user_id: int):
        query = select(models.User).where(models.User.id == user_id)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_user_by_email(self, email: str):
        query = select(models.User).where(models.User.email == email)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def get_users_list(self, skip: int = 0, limit: int = 100):
        query = select(models.User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def create_user(self, user: user_schemas.UserCreate):
        hashed_password = await self.hasher.generate_hash(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=hashed_password)
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def update_user(self, user: user_schemas.UserCreate, user_to_update):
        user_to_update.username = user.username
        user_to_update.email = user.email
        user_to_update.password = await self.hasher.generate_hash(user.password)

        await self.db.commit()
        await self.db.refresh(user_to_update)

        return user_to_update

    async def partly_update_user(self, user: user_schemas.UserPatchUpdate, user_to_update):
        if user.username:
            user_to_update.username = user.username
        if user.email:
            user_to_update.email = user.email
        if user.password:
            user_to_update.password = await self.hasher.generate_hash(user.password)

        await self.db.commit()
        await self.db.refresh(user_to_update)

        return user_to_update

    async def delete_user(self, user_to_delete):
        await self.db.delete(user_to_delete)
        await self.db.commit()
        return user_to_delete


