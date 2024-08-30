from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import model, schemas, utils
from ..database import get_db

routers = APIRouter(
    prefix="/users",
    tags=['Users']
)

@routers.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Userout)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    # print(user.password)
    post = model.User(**user.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post

@routers.get("/{id}", response_model=schemas.Userout)
def get_user_with_id(id: int, db: Session =  Depends(get_db)):
    users = db.query(model.User).filter(model.User.id == id).first()
    if users == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return users