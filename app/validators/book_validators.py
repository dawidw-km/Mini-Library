def title_validator(v: str) ->str:
    """
    Ensures that title is not empty and contains between 2 to 250 characters.
    """
    v = v.strip()
    if not v:
        raise ValueError("Title cannot be empty, please put a real title.")
    elif len(v) < 2 or len(v) > 250:
        raise ValueError("Title can contain between 2 and 250 characters.")
    return v.title()

def pages_validate(v: int) ->int:
    """
    Ensures that pages are not empty and are in range 2 to 2000.
    """
    if v < 2 or v > 2000:
        raise ValueError("Pages must be between 2 to 2000.")
    return v