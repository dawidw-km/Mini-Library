from sqlalchemy.exc import OperationalError
from time import time
from fastapi import FastAPI
from app.api import authors, books, users, rental, token
from app.db.session import SessionLocal
from app.db.seed import seed_admin


app = FastAPI(title="FastAPI Library")

app.include_router(authors.router)

app.include_router(books.router)

app.include_router(users.router)

app.include_router(rental.router)

app.include_router(token.router)

@app.get("/")
async def root():
    return {"Welcome to the Library!": ":)"}
