from sqlmodel import SQLModel, Session, create_engine
from app.config import get_setting

setting = get_setting()
db_url = setting.db_url
engine = create_engine(db_url, connect_args={'check_same_thread': False})


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
