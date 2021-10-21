from fastapi import APIRouter
from ..crud.crud import CRUD
from app.database.database import SessionLocal
from ..schemas import user_schemas
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


crud = CRUD()
router = APIRouter(prefix="/user")


@router.post("/",
             response_model=user_schemas.User,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(db=db, user=user)


@router.get("/user-list/",
            response_model=List[user_schemas.User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud.get_users_list(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}",
            response_model=user_schemas.User)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put('/{user_id}',
            response_model=user_schemas.User)
async def update_user(user_id: int, user: user_schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = await crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.update_user(db=db,
                                  user=user,
                                  user_id=user_id)


@router.patch('/{user_id}',
              response_model=user_schemas.User)
async def partly_update_user(user_id: int, user: user_schemas.UserPatchUpdate, db: Session = Depends(get_db)):
    db_user = await crud.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.partly_update_user(db=db,
                                         user=user,
                                         user_id=user_id)


@router.delete('/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    res = await crud.delete_user(db=db, user_id=user_id)
    if res == "Invalid":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")
    return res
