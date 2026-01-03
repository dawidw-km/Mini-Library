import pytest

def test_create_book_by_id(client):
    get_response = client.post(
        "/authors",
        json={
            "name": "Brandon Sanderson",
            "birth_date": "1997-10-10"
        }
    )
    author_id = get_response.json()["id"]
    response = client.post(
        "/books",
        json={
            "title": "The Way of Kings",
            "pages": 995,
            "author_id": author_id
        }
    )
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "The Way of Kings"
    assert data["pages"] == 995
    assert data["author_id"] == author_id

def test_create_book_by_name(client):
    get_response = client.post(
        "/authors",
        json={
            "name": "David Gemmell",
            "birth_date": "1997-10-10"
        }
    )
    author_name = get_response.json()["name"]
    assert get_response.json()["name"] == author_name
    response = client.post(
        "/books",
        json={
            "title": "The Way of Kings",
            "pages": 995,
            "author_name": "David Gemmell"
        }
    )
    data = response.json()
    assert response.status_code == 201
    assert data["title"] == "The Way of Kings"
    assert data["pages"] == 995
