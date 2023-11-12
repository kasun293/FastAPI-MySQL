from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, SessionLocl
from sqlalchemy.orm import session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class postBase(BaseModel):
    title: str
    content: str
    user_id: int

class UserBase(BaseModel):
    username: str

def get_db():
    db = SessionLocl()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[session, Depends(get_db)]

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: postBase, db: db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()

@app.get("/posts/{post_id}", status_code=status.HTTP_200_OK)
async def read_post(post_id: int, db: db_dependency):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    return post

#delete a record
@app.delete("/post/{post_id}", status_code=status.HTTP_200_OK)
async def delete_post(post_id: int, db:db_dependency):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='post not found')
    db.delete(db_post)
    db.commit()

@app.put("/posts/", status_code=status.HTTP_200_OK)
async def update_post(post: postBase, db:db_dependency):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()

@app.post("/users/", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()

@app.get("/users/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user