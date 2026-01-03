import pytest
from app.validators import general

#Test_Name_Validator

def test_name_validator_invalid_empty():
    with pytest.raises(ValueError, match='Name cannot be empty, please put a real name'):
        general.name_validator("")

def test_name_validator_invalid_length():
    with pytest.raises(ValueError, match='Name must be between 2 and 150 characters'):
        general.name_validator("a")

def test_name_validator_invalid_text():
    with pytest.raises(ValueError, match="Name can contain only letters and spaces"):
        general.name_validator("a12312")

def test_name_validator_valid():
    assert general.name_validator("dawid") == "Dawid"
