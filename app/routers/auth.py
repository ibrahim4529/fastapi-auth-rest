from fastapi import APIRouter, Depends, HTTPException, status
from app.db import get_session
from sqlmodel import Session, select
from app.models import User
from app.utils.hash import verify_password, hash_password
from app.utils.jwt import create_jwt_token, get_active_user
from app.schemas import UserRegister, UserRead, UserToken, UserLogin

router = APIRouter(
    prefix="/auth"
)


def authenticate_user(session: Session,  username: str, password: str):
    statement = select(User).where(User.username == username)
    results = session.exec(statement)
    user = results.first()
    if user is None:
        return False
    if not verify_password(plain_password=password, hashed_password=user.password):
        return False
    return user


@router.post("/login", response_model=UserToken)
def login(*, session: Session = Depends(get_session), form_data: UserLogin):
    user = authenticate_user(session=session, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_jwt_token({"sub": user.username})
    return {
        "user": user,
        "token": token
    }


@router.post("/register", response_model=UserRead)
def register(*, session: Session = Depends(get_session), user: UserRegister):
    db_user = User.from_orm(user)
    db_user.password = hash_password(db_user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.get("/me", response_model=UserRead)
async def me(user: User = Depends(get_active_user)):
    return user
