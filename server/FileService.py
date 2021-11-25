import datetime
import os


def change_dir(path: str, autocreate: bool = True) -> None:
    """Change current directory of app.

    Args:
        path (str): Path to working directory with files.
        autocreate (bool): Create folder if it doesn't exist.

    Raises:
        RuntimeError: if directory does not exist and autocreate is False.
        ValueError: if path is invalid.
    """
    default_path = '/work/files'
    os.chdir(default_path)
    if type(path) != str:
        raise ValueError('path should be string')
    if default_path not in os.path.dirname(path):
        raise ValueError(f'Change dir upper than parent {default_path} is not allowed')
    if not _is_name_valid(path):
        raise ValueError(f'Path {path} is invalid')
    elif os.path.lexists(path):
        os.chdir(path)
    elif autocreate:
        try:
            os.makedirs(path, mode=0o777, exist_ok=False)
            os.chdir(path)
        except (ValueError, FileNotFoundError):
            print(f'Path is invalid: {path}')
    else:
        raise RuntimeError(f'Directory {path} does not exist. Enable autocreate parameter to create it')


def _is_name_valid(name: str) -> bool:
    forbidden_symbols = '<>:"/\|?*'
    name_wo_slashes = name.replace('/', '')
    for symbol in forbidden_symbols:
        if symbol in name_wo_slashes:
            return False
    return True


def get_files() -> list:
    """Get info about all files in working directory.

    Returns:
        List of dicts, which contains info about each file. Keys:
        - name (str): filename
        - create_date (datetime): date of file creation.
        - edit_date (datetime): date of last file modification.
        - size (int): size of file in bytes.
    """
    files_info = []
    file_names = os.listdir(os.getcwd())
    for file_name in file_names:
        files_info.append(get_file_data(file_name))
    return files_info


def get_file_data(filename: str, with_content: bool = False, with_edit_date: bool = True) -> dict:
    """Get full info about file.

    Args:
        filename (str): Filename.
        with_content (bool): return file info with file content
        with_edit_date: (bool):  return file info with edit date
    Returns:
        Dict, which contains full info about file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - edit_date (datetime): date of last file modification
        - size (int): size of file in bytes

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """
    if not _is_name_valid(filename):
        raise ValueError('path is invalid')
    elif os.path.lexists(filename):
        file_info = {'name': filename,
                     'create_date': datetime.datetime.fromtimestamp(os.path.getctime(filename)),
                     'size': os.path.getsize(filename)}
        if with_edit_date:
            file_info['edit_date'] = datetime.datetime.fromtimestamp(os.path.getmtime(filename))
        if with_content:
            with open(filename) as f:
                content = f.read()
            file_info['content'] = content
        return file_info
    else:
        raise RuntimeError(f'File {filename} does not exist')


def create_file(filename: str, content: str = None) -> dict:
    """Create a new file.

    Args:
        filename (str): Filename.
        content (str): String with file content.

    Returns:
        Dict, which contains name of created file. Keys:
        - name (str): filename
        - content (str): file content
        - create_date (datetime): date of file creation
        - size (int): size of file in bytes

    Raises:
        ValueError: if filename is invalid.
    """
    if not _is_name_valid(filename) or not filename.strip():
        raise ValueError('filename is invalid')
    file = open(filename, "w")
    if content:
        file.write(content)
    file.close()
    return get_file_data(file.name, with_content=True, with_edit_date=False)


def delete_file(filename: str) -> None:
    """Delete file.

    Args:
        filename (str): filename

    Raises:
        RuntimeError: if file does not exist.
        ValueError: if filename is invalid.
    """
    if not _is_name_valid(filename):
        raise ValueError(f'filename {filename} is invalid')
    if not os.path.lexists(filename):
        raise FileNotFoundError(f'File {filename} does not exist')
    else:
        if os.path.isdir(filename):
            if os.listdir:
                os.removedirs(filename)
            else:
                os.rmdir(filename)
        else:
            os.remove(filename)
