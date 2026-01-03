from datetime import date

def validate_birth_date(value: date) -> date:
    """
    Ensures that birthdate is not in the future.
    """
    if value > date.today():
        raise ValueError("Date cannot be in the future.")
    return value