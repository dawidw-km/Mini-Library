def title_validator(value: str) ->str:
    """
    Ensures that title is not empty and contains between 2 and 250 characters.
    """
    value = value.strip()
    if not value:
        raise ValueError("Title cannot be empty, please put a real title.")
    elif len(value) < 2 or len(value) > 250:
        raise ValueError("Title can contain between 2 and 250 characters.")
    return value

def pages_validate(value: int) ->int:
    """
    Ensures that pages are not empty and are in range 2 to 2000.
    """
    if value < 2 or value > 2000:
        raise ValueError("Pages must be between 2 and 2000 characters.")
    return value