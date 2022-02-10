from sqlmodel import SQLModel


class UserBase(SQLModel):
    name: str
    username: str


class UserRead(UserBase):
    id: int


class UserRegister(UserBase):
    password: str


class UserToken(SQLModel):
    user: UserRead
    token: str


class UserLogin(SQLModel):
    username: str
    password: str