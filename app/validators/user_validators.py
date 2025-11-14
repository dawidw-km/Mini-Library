from datetime import datetime, date

def ensure_not_empty(value: str, field_name: str):
    value = value.strip()
    if not value:
        raise ValueError(f"Field {field_name} cannot be empty.")
    return value

def ensure_min_length(value: str, field_name: str, *, min_length: int = None):
    if min_length and len(value) < min_length:
        raise ValueError(f"Field {field_name} must contain at least {min_length} characters.")
    return value

def ensure_max_length(value: str, field_name: str, *, max_length: int = None):
    if max_length and len(value) > max_length:
        raise ValueError(f"Field {field_name} must contain at most {max_length} characters.")
    return value

def ensure_alnum(value: str, field_name: str, *, alnum: bool = False) -> str:
    if alnum and not value.isalnum():
        raise ValueError(f"Field {field_name} can contain only alphanumeric characters.")
    return value

def validate_text(value: str, field_name: str, *,
                 min_length: int = None,
                 max_length: int = None,
                 alnum: bool = False) -> str:
    value = ensure_not_empty(value, field_name)
    value = ensure_min_length(value, field_name, min_length=min_length)
    value = ensure_max_length(value, field_name, max_length=max_length)
    value = ensure_alnum(value, field_name, alnum=alnum)
    return value


def birth_date_validator(v: str) ->str:
    if isinstance(v, str):
        try:
            v = datetime.strptime(v.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("Wrong format, try again. (e.g 2000-12-31)")
    elif not isinstance(v, date):
        raise ValueError("Birth date must be a valid date.")

    if v > date.today():
        raise ValueError("Date cannot be in the future.")
    if v < date(1900, 1, 1):
        raise ValueError("Birth date seems too old, please try again.")

    return v