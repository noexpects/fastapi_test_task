from sqlalchemy.orm import Session
from app import models, schemas


def get_hashed_password(password: str):
    password += "xXxyYyNOTREALHASHyYyxXx"
    return password


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = get_hashed_password(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()
    user_to_update.username = user.username
    user_to_update.email = user.email
    user_to_update.password = get_hashed_password(user.password)

    db.commit()
    db.refresh(user_to_update)

    return user_to_update


def partly_update_user(db: Session, user: schemas.UserPatchUpdate, user_id:int):
    user_to_update = db.query(models.User).filter(models.User.id == user_id).first()

    if user.username:
        user_to_update.username = user.username
    if user.email:
        user_to_update.email = user.email
    if user.password:
        user_to_update.password = get_hashed_password(user.password)

    db.commit()
    db.refresh(user_to_update)

    return user_to_update


def delete_user(db: Session, user_id: int):
    user_to_delete = db.query(models.User).filter(models.User.id == user_id).first()
    if user_to_delete is None:
        return "Invalid"
    else:
        db.delete(user_to_delete)
        db.commit()

    return user_to_delete


