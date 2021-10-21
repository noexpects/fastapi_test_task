from sqlalchemy.orm import Session
from ..models import models
from ..schemas import user_schemas


class CRUD:

    async def get_hashed_password(self, password: str):
        password += "xXxyYyNOTREALHASHyYyxXx"
        return password

    async def get_user(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    async def get_user_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    async def get_users_list(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    async def create_user(self, db: Session, user: user_schemas.UserCreate):
        fake_hashed_password = await self.get_hashed_password(user.password)
        db_user = models.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    async def update_user(self, db: Session, user: user_schemas.UserCreate, user_id: int):
        user_to_update = db.query(models.User).filter(models.User.id == user_id).first()
        user_to_update.username = user.username
        user_to_update.email = user.email
        user_to_update.password = await self.get_hashed_password(user.password)

        db.commit()
        db.refresh(user_to_update)

        return user_to_update

    async def partly_update_user(self, db: Session, user: user_schemas.UserPatchUpdate, user_id:int):
        user_to_update = db.query(models.User).filter(models.User.id == user_id).first()

        if user.username:
            user_to_update.username = user.username
        if user.email:
            user_to_update.email = user.email
        if user.password:
            user_to_update.password = await self.get_hashed_password(user.password)

        db.commit()
        db.refresh(user_to_update)

        return user_to_update

    async def delete_user(self, db: Session, user_id: int):
        user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
        if user_to_delete is None:
            return "Invalid"
        else:
            db.delete(user_to_delete)
            db.commit()

        return user_to_delete


