from datetime import datetime, date

def name_validator(value: str) ->str:
    """
    Ensures that name is not empty and has proper length.
    """
    value = value.strip()
    if not value:
        raise ValueError('Name cannot be empty, please put a real name.')
    elif len(value) < 2 or len(value) > 150:
        raise ValueError('Name must be between 2 and 150 characters.')
    elif not value.replace(" ", "").isalpha():
        raise ValueError("Name can contain only letters and spaces")
    return value.title()

def update_validator(model):
    data = model.model_dump(exclude_unset=True)
    if not data:
        raise ValueError("At least one of the fields is required")