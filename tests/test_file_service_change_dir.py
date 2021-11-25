import os

import pytest

from server import FileService

default_path = '/work/files'


@pytest.fixture()
def create_and_delete_dir():
    path = '/work/files/n'
    while os.path.lexists(path):
        path += 'n'
    yield path
    if os.path.lexists(path):
        os.rmdir(path)


def test_change_dir_existing():
    FileService.change_dir('/work/files/rt')
    assert os.getcwd() == '/work/files/rt'


def test_change_dir_create(create_and_delete_dir):
    FileService.change_dir(create_and_delete_dir)
    assert os.getcwd() == create_and_delete_dir


def test_change_dir_upper():
    with pytest.raises(ValueError):
        FileService.change_dir('/work/aaa')


def test_change_dir_level_up_upper_than_allowed():
    with pytest.raises(ValueError):
        FileService.change_dir('..')


def test_change_dir_level_up_upper_allowed():
    FileService.change_dir('/work/files/rt')
    FileService.change_dir('..')
    assert os.getcwd() == default_path


def test_change_dir_invalid():
    with pytest.raises(ValueError):
        FileService.change_dir('/work/files/%?<>')


def test_change_dir_autocreate_false():
    with pytest.raises(RuntimeError):
        FileService.change_dir('/work/files/abab', autocreate=False)


def test_change_dir_empty_path():
    with pytest.raises(ValueError):
        FileService.change_dir('')


def test_change_dir_path_none():
    with pytest.raises(ValueError):
        FileService.change_dir(None)


def test_change_dir_path_non_str():
    with pytest.raises(ValueError):
        FileService.change_dir(5)
