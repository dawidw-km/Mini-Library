import pytest

from app.validators import author_validators
from datetime import date

@pytest.mark.parametrize(
    "value",
    [
        date(1997, 4, 10),
        date(1950, 5, 10),
        date(2001, 6, 10),
    ]
)
def test_author_for_valid_birth_date(value):
    result = author_validators.validate_birth_date(value)
    assert result == value

def test_author_for_invalid_birth_date():
    with pytest.raises(ValueError):
        author_validators.validate_birth_date(date(2050, 4, 10))