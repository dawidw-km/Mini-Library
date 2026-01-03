import pytest

from app.validators import book_validators

def test_book_title_empty():
    with pytest.raises(ValueError, match='Title cannot be empty, please put a real title'):
        book_validators.title_validator("")

def test_book_title_short_length():
    with pytest.raises(ValueError, match='Title can contain between 2 and 250 characters.'):
        book_validators.title_validator("a")

def test_book_title_long_length():
    with pytest.raises(ValueError, match='Title can contain between 2 and 250 characters.'):
        book_validators.title_validator("a" * 251)

def test_book_title_whitespace():
    assert book_validators.title_validator(" Wind and Truth ") == "Wind and Truth"

def test_book_title_valid():
    assert book_validators.title_validator("Wind and Truth") == "Wind and Truth"

def test_book_page_too_many():
    with pytest.raises(ValueError, match='Pages must be between 2 and 2000 characters.'):
        book_validators.pages_validate(200100)

def test_book_page_too_little():
    with pytest.raises(ValueError, match='Pages must be between 2 and 2000 characters.'):
        book_validators.pages_validate(1)

def test_book_page_valid():
    assert book_validators.pages_validate(300) == 300