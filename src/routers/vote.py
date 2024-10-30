from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..oauth2 import get_current_user
from ..schemas import Vote

router = APIRouter(prefix="/vote", tags=["votes"])


@router.post("/", status_code=201)
def vote(
    vote: Vote, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post does not exist")

    vote_query = (
        select(models.Vote)
        .where(models.Vote.post_id == vote.post_id)
        .where(models.Vote.user_id == current_user.id)
    )
    found_vote = db.execute(vote_query).scalars().first()

    if vote.direction == 1:
        if found_vote:
            raise HTTPException(
                status_code=409,
                detail=f"user {current_user.id} has already voted on post {vote.post_id}",
            )
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}

    else:
        if not found_vote:
            raise HTTPException(status_code=404, detail=f"vote does not exist")

        db.delete(found_vote)
        db.commit()
        return {"message": "successfully deleted vote"}
