from fastapi import FastAPI
from app.api import authors, books, users

app = FastAPI(title="FastAPI Library")

app.include_router(authors.router)
app.include_router(books.router)

app.include_router(users.router)

@app.get("/")
def root():
    return {"message": "Result"}