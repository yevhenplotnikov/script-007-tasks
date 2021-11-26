import os

import pytest

from server import FileService
from utils import FileUtils as utils


default_path = 'files'
global current_working_dir


@pytest.fixture(scope='module')
def current_working_dir_fixt():
    return current_working_dir


@pytest.fixture(scope='module', autouse=True)
def create_and_clean_up_default_path():
    FileService.change_dir(default_path)
    global current_working_dir
    current_working_dir = os.getcwd()
    yield
    FileService.change_dir(current_working_dir)
    FileService.change_dir('..')
    utils.delete_dir(default_path)
