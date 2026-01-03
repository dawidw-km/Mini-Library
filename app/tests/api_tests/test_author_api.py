import pytest

def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome to the Library!": ":)"}

def test_create_author(client):
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
def test_create_author_duplicate(input_name, input_birth_date, expected_value, client):
    response = client.post(
        "/authors",
        json={
            "name": input_name,
            "birth_date": input_birth_date
        }
    )
    assert response.status_code == expected_value


def test_create_author_response_body(client):
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

def test_soft_delete_author_successful(client):
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

def test_soft_delete_author_404(client):
    response = client.delete(
        "/authors/1111",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"

def test_author_partial_update(client):
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

def test_author_partial_update_invalid(client):
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

def test_non_existent_author(client):
    response = client.get("/authors/999")
    assert response.status_code == 404

def test_patch_soft_deleted_author(client):
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

def test_double_delete_author(client):
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