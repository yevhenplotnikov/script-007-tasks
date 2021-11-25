import os

import pytest

from server import FileService

default_path = '/work/files'
new_file_name = 'new1'
new_file_content = 'content1'
multiple_files = {'new2': 'content2', 'new3': 'content3', 'new4': 'content4'}


@pytest.fixture(autouse=True)
def change_to_default_folder():
    FileService.change_dir('/work/files/')


@pytest.fixture()
def create_file():
    FileService.create_file(new_file_name, new_file_content)


@pytest.fixture()
def create_multiple_files():
    FileService.change_dir('/work/files/multiple')
    for name, content in multiple_files.items():
        FileService.create_file(name, content)
    yield
    for name in multiple_files.keys():
        FileService.delete_file(name)
    FileService.change_dir('/work/files/')
    FileService.delete_file('multiple')


@pytest.fixture()
def delete_file_after_test():
    yield
    FileService.delete_file(new_file_name)


@pytest.fixture()
def delete_file():
    FileService.delete_file(new_file_name)


def test_create_file_positive(create_file, delete_file_after_test):
    data = FileService.get_file_data(new_file_name, with_content=True)
    assert data['name'] == new_file_name
    assert data['content'] == new_file_content


def test_create_file_invalid_name():
    with pytest.raises(ValueError):
        FileService.create_file('***')


def test_create_file_empty_name():
    with pytest.raises(ValueError):
        FileService.create_file('')


def test_delete_file_positive(create_file, delete_file):
    assert not os.path.lexists(new_file_name)


def test_delete_not_existing_file():
    with pytest.raises(FileNotFoundError):
        FileService.delete_file('asfsgdsfg')


def test_get_file_data(create_multiple_files):
    actual_data = [file['name'] for file in FileService.get_files()]
    assert sorted(actual_data) == sorted(list(multiple_files.keys()))
