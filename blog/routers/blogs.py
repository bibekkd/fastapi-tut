from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional, List
from .. import schema, models
from sqlalchemy.orm import Session
from ..database import get_db
from ..oauth2 import get_current_user

router = APIRouter(
    prefix="/blog",
    tags=["Blogs"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schema.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/blogs", response_model=List[schema.ShowBlog], tags=["Blogs"])
def all_blogs(db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{id}", status_code=200, response_model=schema.ShowBlog)
def blog(id: int, response: Response, db: Session = Depends(get_db), current_user: schema.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    return blog


@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
def update(id: int, request: schema.Blog, db: Session = Depends(get_db)):
    blog_q = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blog_q.update({"title": request.title, "body": request.body})
    db.commit()
    return "updated successfully"


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db)):
    blog_q = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog_q.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with the id {id} not found")
    blog_q.delete()
    db.commit()
    return
