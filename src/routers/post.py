from fastapi import HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from sqlalchemy import select

from ..oauth2 import get_current_user
from ..schemas import Post, PostCreate
from .. import models
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get("/", response_model=dict[str, str | list[Post]])
def get_posts_range(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    limit: int = 10,
    skip: int = 0,
):
    posts = (
        db.execute(
            select(models.Post)
            .order_by(models.Post.created_at.desc())
            .limit(limit)
            .offset(skip)
        )
        .scalars()
        .all()
    )
    response_body = {"count": f"{len(posts)}", "posts": posts}
    return response_body


@router.get("/latest", response_model=list[Post])
def get_latest_posts(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    limit: int = 10,
):
    posts = (
        db.execute(
            select(models.Post).order_by(models.Post.created_at.desc()).limit(limit)
        )
        .scalars()
        .all()
    )
    if not posts:
        raise HTTPException(status_code=404, detail="No posts available")
    return posts


@router.get("/{id}", response_model=Post)
def get_post_by_id(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404)
    return post


@router.post("/", status_code=201, response_model=Post)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    new_post = models.Post(author_id=current_user.id, **post.model_dump())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{id}", response_model=Post)
def update_post(
    id: int,
    updated_post: PostCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    print(current_user)
    if post == None:
        raise HTTPException(status_code=404, detail=f"post with id {id} does not exist")

    post_query.update(updated_post.model_dump(), synchronize_session=False)  # type: ignore
    db.commit()

    return post_query.first()


@router.delete("/{id}", status_code=204)
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=404, detail="post does not exist")

    if post.author_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="not authorized to perform this action"
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=204)
