import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.session import get_db
from app.db.base import Base
from sqlalchemy.pool import StaticPool
from app.security.jwt_u import get_current_user

DATABASE_URL = "sqlite:///:memory:"

engine_test = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

class FakeUser:
    def __init__(self):
        self.id = 1
        self.role = "admin"

def override_get_current_user():
    return FakeUser()


app.dependency_overrides[get_db] = override_get_db

app.dependency_overrides[get_current_user] = override_get_current_user

Base.metadata.create_all(bind=engine_test)

@pytest.fixture(scope="session")
def client():
    return TestClient(app)