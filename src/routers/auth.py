from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, HTTPException
from ..schemas import UserOut, UserLogin, Token
from ..utils import verify
from ..database import get_db
from ..models import User as UserModel
from ..oauth2 import create_access_token
from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=Token)
def user_login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):

    user = (
        db.query(UserModel).filter(UserModel.email == user_credentials.username).first()
    )

    if not user:
        raise HTTPException(status_code=403, detail="invalid credentials")

    if not verify(user_credentials.password, str(user.password)):
        raise HTTPException(status_code=403, detail="incorrect credentials")

    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
