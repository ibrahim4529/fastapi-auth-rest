from jose import JWTError, jwt
from datetime import timedelta, datetime
from app.config import get_setting
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from sqlmodel import Session, select
from app.db import get_session
from app.models import User

config = get_setting()
oauth2_scheme = HTTPBearer()
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"Authorization": "Bearer"},
)


def create_jwt_token(payload: dict) -> str:
    expire = datetime.utcnow() + timedelta(hours=config.jwt_expire_time_hour)
    to_encode = payload.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.jwt_secret, algorithm=config.jwt_algorithm)
    return encoded_jwt


def get_username_from_token(token: str):
    username: str
    try:
        payload = jwt.decode(token, config.jwt_secret, algorithms=[config.jwt_algorithm])
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username


async def get_active_user(session: Session = Depends(get_session),
                          credentials=Depends(oauth2_scheme)):
    username = get_username_from_token(credentials.credentials)
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    if user is None:
        raise credentials_exception
    return user
