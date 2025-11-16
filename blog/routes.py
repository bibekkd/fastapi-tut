from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from . import schema, models
from .database import SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get("/blogs", response_model=List[schema.ShowBlog], tags=["Blogs"])
def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get("/blog/{id}", status_code=200, response_model=schema.ShowBlog, tags=["Blogs"])
def blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"detail": f"Blog with the {id} not found"}
    return blog

@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Blogs"])
def update(id: int, request: schema.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blog.update({"title": request.title, "body": request.body})
    db.commit()
    return "updated successfully"

@router.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
def delete(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blog.delete()
    db.commit()
    return 


def get_pwd_context():
    # create CryptContext lazily to avoid running backend-detection at import time
    # Use pbkdf2_sha256 to avoid native `bcrypt` backend/version detection issues
    return CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


@router.post("/user", status_code=status.HTTP_201_CREATED, response_model=schema.ShowUser, tags=["Users"])
def create_user(request: schema.User, db: Session = Depends(get_db)):
    pwd_context = get_pwd_context()

    # pbkdf2_sha256 accepts arbitrary-length passwords, so hash directly.
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

@router.get("/user/{id}", status_code=200, response_model=schema.ShowUser, tags=["Users"])
def user(id: int, response: Response, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    return user

@router.put("/user/{id}", status_code=status.HTTP_202_ACCEPTED, tags=["Users"])
def update_user(id: int, request: schema.User, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id)
    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the id {id} not found")
    pwd_context = get_pwd_context()
    hashed_password = pwd_context.hash(request.password)
    user.update({"username": request.username, "email": request.email, "password": hashed_password})
    db.commit()
    return "updated successfully"