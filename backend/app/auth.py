from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from .database import get_db
from .models import User


SECRET_KEY = "change-this-secret-key-later"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60


password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="login"
)


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:

    return password_hash.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
    username: str
) -> str:

    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    data = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        data,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={
            "WWW-Authenticate": "Bearer"
        }
    )

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username is None:
            raise credentials_exception

    except JWTError:

        raise credentials_exception

    user = (
        db.query(User)
        .filter(User.username == username)
        .first()
    )

    if user is None:
        raise credentials_exception

    return user