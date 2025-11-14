from datetime import date

def validate_birth_date(v: date) -> date:
    """
    Ensures that birthdate is not in the future.
    """
    if v > date.today():
        raise ValueError("Date cannot be in the future.")
    return v