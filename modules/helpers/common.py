"""Contains various helper functions."""

__all__: list[str] = ["is_valid_string"]


def is_valid_string(value: str) -> bool:
    """Validates if a string is not None and is not empty.

    Args:
        value: the string to validate

    Returns:
        True if value is not None, is an instance of class str
        and is not equal to "".
    """
    return value is not None and isinstance(value, str) and value != ""
