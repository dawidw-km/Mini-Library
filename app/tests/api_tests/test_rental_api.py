import pytest
from datetime import date

def test_add_rental_twice(client):
    create_author = client.post(
        "/authors",
        json={
            "name": "Johnny Depp",
            "birth_date": "1997-10-10"
        }
    )

    author_id = create_author.json()["id"]
    create_book = client.post(
        "/books",
        json={
            "title": "The Way of Pigs",
            "pages": 995,
            "author_id": author_id
        }
    )
    
    create_user = client.post(
        "/users",
        json={
            "login": "polska123",
            "password": "polska12345",
            "full_name": "John Johnecki",
            "birth_date": "1997-10-10",
            "city": "Wrocław",
            "street": "Psie Pole",
            "postal_code": "12345",
            "address_email": "example@gmail.com"
        }
    )
    
    
    book_id = create_book.json()["id"]
    user_id = create_user.json()["id"]
    create_rental = client.post(
        "/rentals",
        json={
            "user_reader_id": user_id,
            "book_id": book_id
        }
    )
    
    create_rental_2 = client.post(
        "/rentals",
        json={
            "user_reader_id": user_id,
            "book_id": book_id
        }
    )
    assert create_author.status_code == 201
    assert create_book.status_code == 201
    assert create_user.status_code == 201

    assert create_rental.status_code == 201
    assert create_rental_2.status_code == 409
    
    
def test_return_rental_sets_worker_and_frees_book(client):
    author = client.post("/authors", json={
        "name": "Test Author",
        "birth_date": "1990-01-01"
    })
    author_id = author.json()["id"]

    book = client.post("/books", json={
        "title": "Test Book",
        "pages": 100,
        "author_id": author_id
    })
    book_id = book.json()["id"]

    reader = client.post("/users", json={
        "login": "reader1",
        "password": "readerpass",
        "full_name": "Reader One",
        "birth_date": "1995-01-01",
        "city": "City",
        "street": "Street",
        "postal_code": "00-000",
        "address_email": "reader@example.com"
    })
    reader_id = reader.json()["id"]

    worker = client.post("/users", json={
        "login": "worker1",
        "password": "workerpass",
        "full_name": "Worker One",
        "birth_date": "1985-01-01",
        "city": "City",
        "street": "Street",
        "postal_code": "00-000",
        "address_email": "worker@example.com"
    })
    worker_id = worker.json()["id"]

    rental = client.post("/rentals", json={
        "user_reader_id": reader_id,
        "book_id": book_id
    })
    assert rental.status_code == 201
    rental_id = rental.json()["id"]

    returned = client.patch(f"/rentals/{rental_id}/return", json={
        "user_worker_id": worker_id
    })

    assert returned.status_code == 200
    data = returned.json()

    assert data["return_date"] is not None
    assert data["is_rented"] is False

    assert data["user_worker_id"] == worker_id

    second_rental = client.post("/rentals", json={
        "user_reader_id": reader_id,
        "book_id": book_id
    })
    assert second_rental.status_code == 201
