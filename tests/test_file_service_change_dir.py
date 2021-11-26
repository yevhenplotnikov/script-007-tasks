import os

import pytest

from server import FileService
from utils import FileUtils as utils


@pytest.fixture()
def create_and_delete_dir(current_working_dir_fixt):
    path = 'n'
    yield path
    FileService.change_dir(current_working_dir_fixt)
    utils.delete_dir(path)


def test_change_dir_create(create_and_delete_dir):
    current_path = os.getcwd()
    FileService.change_dir(create_and_delete_dir)
    assert os.getcwd() == current_path + '/' + create_and_delete_dir


def test_change_dir_level_up():
    current_path = os.getcwd()
    FileService.change_dir('rt')
    FileService.change_dir('..')
    assert os.getcwd() == current_path


def test_change_dir_invalid():
    with pytest.raises(ValueError):
        FileService.change_dir('files/%?<>')


def test_change_dir_autocreate_false():
    with pytest.raises(RuntimeError):
        FileService.change_dir('files/abab', autocreate=False)


def test_change_dir_empty_path():
    with pytest.raises(ValueError):
        FileService.change_dir('')


def test_change_dir_path_none():
    with pytest.raises(ValueError):
        FileService.change_dir(None)


def test_change_dir_path_non_str():
    with pytest.raises(ValueError):
        FileService.change_dir(5)
