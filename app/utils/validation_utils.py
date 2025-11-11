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