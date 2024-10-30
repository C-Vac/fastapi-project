from sqlalchemy.orm import Session

from fastapi import FastAPI, HTTPException, Depends, APIRouter

from ..oauth2 import get_current_user
from ..schemas import UserCreate, UserOut, UserAndProfile
from .. import models, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", status_code=201, response_model=UserAndProfile)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user.

    Args:
        user (UserCreate): The user to create.
        db (Session): The database session.

    Raises:
        HTTPException: If a user with the given email address already exists.
    """
    existing_user = (
        db.query(models.User).filter(models.User.email == user.email).first()
    )
    if existing_user:
        raise HTTPException(
            status_code=400, detail="user with that email address already exists"
        )

    hashed_pw = utils.hash(user.password)
    new_user = models.User(email=user.email, password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    new_profile = models.UserProfile(username=user.username, user_id=new_user.id)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    return {"user": new_user, "profile": new_profile}


@router.get("/{id}", response_model=UserOut)
def get_user(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Retrieves a user by their id.

    Args:
        id (int): The id of the user to retrieve.
        db (Session): The database session.
        current_user (models.User): The current user.

    Raises:
        HTTPException: If the user does not exist.

    Returns:
        models.User: The retrieved user.
    """
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=404, detail=f"user with id: {id} does not exist"
        )

    return user
