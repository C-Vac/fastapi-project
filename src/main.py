from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from .schemas import *
from .database import engine, get_db
from . import models
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
def root(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts
