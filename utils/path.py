from pathlib import Path


def get_current_dir(file):
    """
    Returns path to the current directory
    Usage: get_current_dir(__file__)
    """
    return Path(file).resolve().parent
