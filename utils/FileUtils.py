import os
import shutil


def delete_dir(dirname: str) -> None:
    """Deletes directory no matter it contains something or not.

    Args:
        dirname (str): dirname

    Raises:
        FileNotFoundError: if directory does not exist.
        ValueError: if directory is invalid.
    """
    if not is_name_valid(dirname):
        raise ValueError(f'dirname {dirname} is invalid')
    if not os.path.exists(dirname):
        raise FileNotFoundError(f'File {dirname} does not exist')
    if not os.path.isdir(dirname):
        raise ValueError(f'{dirname} is not a directory')
    if os.listdir(dirname):
        shutil.rmtree(dirname)
    else:
        os.rmdir(dirname)


def is_name_valid(name: str) -> bool:
    forbidden_symbols = '<>:"\|?*'
    for symbol in forbidden_symbols:
        if symbol in name:
            return False
    if name == '':
        return False
    return True