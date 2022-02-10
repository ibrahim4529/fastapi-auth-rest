from fastapi import FastAPI
from app.routers import auth
from app.db import create_db_and_tables


app = FastAPI()
app.include_router(auth.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
