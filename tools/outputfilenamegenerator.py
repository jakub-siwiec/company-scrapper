import time


def _name_string_operation(name):
    """Add timestamp before the extension.

    Args:
        name (string): Filename with a timestamp to output.

    Returns:
        string or None: New filename string if there is an extension. None if there is no extension.
    """
    if "." in name:
        idx = name.index(".")
        timestring = time.strftime("%Y%m%d%H%M%S")
        return name[:idx] + timestring + name[idx:]
    else:
        return None


def _add_suffix_to_the_end(name):
    """Add suffix to the end in the case of no extension.

    Args:
        name (string): Filename with a timestamp to output.

    Returns:
        string: New filename with a timestamp suffix.
    """
    timestring = time.strftime("%Y%m%d%H%M%S")
    return name + timestring


def generate_name(name):
    """Generate the name with a time suffix in the end of the filename (before extension).

    Args:
        name (string): Current custom filename.

    Returns:
        string: New filename with a timestamp.
    """
    res = _name_string_operation(name)
    if res is not None:
        return res
    else:
        return _add_suffix_to_the_end(name)
