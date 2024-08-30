from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import List
from random import randrange
from sqlalchemy.orm import Session
from . import model, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.routers)
app.include_router(user.routers)
app.include_router(auth.routers)