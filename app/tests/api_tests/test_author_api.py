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

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome to the Library!": ":)"}

def test_create_author():
    response = client.post(
        "/authors",
        json={
            "name": "John Snow",
            "birth_date": "1997-10-10"
        }
    )
    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "name": "John Snow",
        "birth_date": "1997-10-10"
    }

    response = client.post(
        "/authors",
        json={
            "name": "John Snow",
            "birth_date": "1997-10-10"
        }
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Author with that name already exists."}

@pytest.mark.parametrize(
    "input_name, input_birth_date, expected_value",
    [
        ("Mike Johnson", "2000-01-01", 201),
        ("Mike Johnson", "2000-01-01", 400),
    ]
)
def test_create_author_duplicate(input_name, input_birth_date, expected_value):
    response = client.post(
        "/authors",
        json={
            "name": input_name,
            "birth_date": input_birth_date
        }
    )
    assert response.status_code == expected_value


def test_create_author_response_body():
    response = client.post(
        "/authors",
        json={
            "name": "Dawid Pierwszy",
            "birth_date": "1997-10-10"
        }
    )
    data = response.json()

    assert data["name"] == "Dawid Pierwszy"
    assert data["birth_date"] == "1997-10-10"
    assert isinstance(data["id"], int)

def test_soft_delete_author_successful():
    create_response = client.post(
        "/authors",
        json={
            "name": "Jan Kowalski",
            "birth_date": "1997-10-10"
        }
    )
    author_id = create_response.json()["id"]

    response = client.delete(
        f"/authors/{author_id}",
    )
    assert response.status_code == 204

def test_soft_delete_author_404():
    response = client.delete(
        "/authors/1111",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"

def test_author_partial_update():
    create_response = client.post(
        "/authors",
        json={
            "name": "Janek Kowalski",
            "birth_date": "1997-10-10"
        }
    )
    author_id = create_response.json()["id"]
    response = client.patch(
        f"/authors/{author_id}",
        json={
            "name": "Marcin Sroka",
        }
    )
    assert response.status_code == 200

def test_author_partial_update_invalid():
    create_response = client.post(
        "/authors",
        json={
            "name": "Marek Kowalski",
            "birth_date": "1997-10-10"
        }
    )
    author_id = create_response.json()["id"]
    response = client.patch(
        f"/authors/{author_id}",
        json={

        }
    )
    assert response.status_code == 422

def test_non_existent_author():
    response = client.get("/authors/999")
    assert response.status_code == 404

def test_patch_soft_deleted_author():
    create_response = client.post(
        "/authors",
        json={
            "name": "John Cena",
            "birth_date": "1997-10-10"
        }
    )
    author_id = create_response.json()["id"]
    response = client.delete(
        f"/authors/{author_id}",
    )
    response = client.patch(
        f"/authors/{author_id}",
        json={
            "name": "John See",
        }
    )
    assert response.status_code == 404

def test_double_delete_author():
    create_response = client.post(
        "/authors",
        json={
            "name": "Mike Tyson",
            "birth_date": "1997-10-10"
        }
    )
    author_id = create_response.json()["id"]
    response = client.delete(
        f"/authors/{author_id}",
    )
    assert response.status_code == 204
    response = client.delete(
        f"/authors/{author_id}",
    )
    assert response.status_code == 404