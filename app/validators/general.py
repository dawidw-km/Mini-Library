from datetime import datetime, date

def name_validator(v: str) ->str:
    """
    Ensures that name is not empty and has proper length.
    """
    v = v.strip()
    if not v:
        raise ValueError('Name cannot be empty, please put a real name.')
    elif len(v) < 2 or len(v) > 150:
        raise ValueError('Name must be between 2 and 150 characters.')
    elif not v.replace(" ", "").isalpha():
        raise ValueError("Name can contain only letters and spaces")
    return v.title()

def birth_date_name_parsed(v: str) -> date:
    """
    Ensures that the birthdate is in the correct format 'YYYY-MM-DD'.
    """
    if isinstance(v, str):
        try:
            return datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError("Date must be in correct format YYYY-MM-DD (e.g) 1997-04-10")
    return v
