def read_file(path: str):
    """Reads a file on the given path

    Args:
        path (str): the path to the file

    Returns:
        str: the contents of the file
    """
    # read the contents of the file
    with open(path, "r", encoding="utf-8") as file:
        data = file

    return data
