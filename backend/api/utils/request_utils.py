def check_not_none(*args) -> None:
    if not all(arg is not None for arg in args):
        raise Exception
