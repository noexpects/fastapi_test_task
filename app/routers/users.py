from fastapi import APIRouter
from app.services.crud.user_crud import CRUD
from app.database.database import SessionLocal
from ..schemas import user_schemas
from fastapi import HTTPException, status
from typing import List


# Dependency
def get_db():
    db = SessionLocal()
    return db


crud = CRUD(db=get_db())
router = APIRouter(prefix="/user")


@router.post("/",
             response_model=user_schemas.User,
             status_code=status.HTTP_201_CREATED)
async def create_user(user: user_schemas.UserCreate):
    db_user = await crud.get_user_by_email(email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return await crud.create_user(user=user)


@router.get("/user-list/",
            response_model=List[user_schemas.User])
async def read_users(skip: int = 0, limit: int = 100):
    users = await crud.get_users_list(skip=skip, limit=limit)
    return users


@router.get("/{user_id}",
            response_model=user_schemas.User)
async def read_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put('/{user_id}',
            response_model=user_schemas.User)
async def update_user(user_id: int, user: user_schemas.UserCreate):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.update_user(user=user,
                                  user_to_update=db_user)


@router.patch('/{user_id}',
              response_model=user_schemas.User)
async def partly_update_user(user_id: int, user: user_schemas.UserPatchUpdate):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.partly_update_user(user=user,
                                         user_to_update=db_user)


@router.delete('/{user_id}')
async def delete_user(user_id: int):
    db_user = await crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return await crud.delete_user(db_user)
