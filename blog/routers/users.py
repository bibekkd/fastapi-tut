from fastapi import APIRouter, Depends, status, HTTPException
from typing import List
from sqlalchemy.orm import Session
from .. import schema, models
from ..deps import get_pwd_context
from ..database import get_db

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.ShowUser)
def create_user(request: schema.User, db: Session = Depends(get_db)):
    pwd_context = get_pwd_context()
    hashed_password = pwd_context.hash(request.password)
    new_user = models.User(username=request.username, email=request.email, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users", response_model=List[schema.ShowUser], tags=["Users"])
def all_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", status_code=200, response_model=schema.ShowUser)
def user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    return user


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(id: int, request: schema.User, db: Session = Depends(get_db)):
    user_q = db.query(models.User).filter(models.User.id == id)
    if not user_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    pwd_context = get_pwd_context()
    hashed_password = pwd_context.hash(request.password)
    user_q.update({"username": request.username, "email": request.email, "password": hashed_password})
    db.commit()
    return "updated successfully"
