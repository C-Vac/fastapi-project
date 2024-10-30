from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

ACCESS_TOKEN_EXPIRE_MINUTES = 60
ALGORITHM = "HS256"
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    """
    Creates a JWT token that expires in ACCESS_TOKEN_EXPIRE_MINUTES minutes.

    Args:
        data (dict): The data to encode in the JWT token.

    Returns:
        str: The encoded JWT token.
    """
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    """
    Verifies the given JWT token and returns the user_id if the token is valid.

    Args:
        token (str): The JWT token to verify.
        credentials_exception (fastapi.HTTPException): The exception to raise if the token is invalid.

    Returns:
        schemas.TokenData: The user_id encoded in the JWT token.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        id = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=str(id))

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    """
    Retrieves the current user from the database using the provided JWT token.

    This function depends on `oauth2_scheme` to extract the token and
    `database.get_db` to get the database session. It verifies the token,
    raises an HTTP exception if the token is invalid, and returns the corresponding user.

    Args:
        token (str): The JWT token extracted from the request header.
        db (Session): SQLAlchemy database session.

    Returns:
        models.User: The user associated with the token.

    Raises:
        HTTPException: If the token is invalid or the user does not exist.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="could not validate user credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == int(token_data.id)).first()  # type: ignore

    return user
