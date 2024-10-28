from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Depends, APIRouter
from ..schemas import Post, PostCreate
from .. import models, utils
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=list[Post])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.get("/latest")  # TODO need work
def get_latest_post(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()

    return posts


@router.get("/{id}", response_model=Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404)
    return post


@router.post("/", status_code=201, response_model=Post)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=Post)
def update_post(id: int, updated_post: PostCreate, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} does not exist")

    post_query.update(updated_post.model_dump(), synchronize_session=False)  # type: ignore
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=404)
    post.delete(synchronize_session=False)
    db.commit()
    return
