from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Depends, APIRouter

from ..oauth2 import get_current_user
from ..schemas import UserCreate, UserOut
from .. import models, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="user with that email address already exists"
        )

    hashed_pw = utils.hash(user.password)
    user.password = hashed_pw
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}", response_model=UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"user with id: {id} does not exist"
        )

    return user
