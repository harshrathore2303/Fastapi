from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from random import randrange
from .. import model, schemas, oauth2
from ..database import get_db

routers = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@routers.get("/", response_model=List[schemas.Post])
def get_post(db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    posts = db.query(model.Post).all()
    # print(posts)
    return posts

@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # print(post.dict())
    print(user_id)
    posts = model.Post(**post.dict())
    # print(posts)
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts

@routers.get("/{id}", response_model=schemas.Post)
def get_posts_with_id(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post = db.query(model.Post).filter(model.Post.id == id).first()
    print(post)
    if not post:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    return post

@routers.delete("/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    del_post = db.query(model.Post).filter(model.Post.id == id)
    print(del_post)
    if del_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    del_post.delete(synchronize_session=False)
    db.commit()
    return {"data": "deleted"}

@routers.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    post_query = db.query(model.Post).filter(model.Post.id == id)
    post = post_query.first()
    if (post == None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post
