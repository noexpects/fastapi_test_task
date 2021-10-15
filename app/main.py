from typing import List

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from app import models, crud, schemas
from app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/user/",
          response_model=schemas.User,
          status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/user-list/",
         response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users_list(db, skip=skip, limit=limit)
    return users


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.put('/user/{user_id}', response_model=schemas.User)
def update_user(user_id:int, user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db=db, user=user, user_id=user_id)


@app.patch('/user/{user_id}', response_model=schemas.User)
def partly_update_user(user_id:int, user: schemas.UserPatchUpdate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.partly_update_user(db=db, user=user, user_id=user_id)


@app.delete('/user/{user_id}')
def delete_user(user_id: int, db: Session= Depends(get_db)):
    res = crud.delete_user(db=db, user_id=user_id)
    if res == "Invalid":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return res


