import os
import rookit.files

DATA = os.path.join(os.path.dirname(__file__), 'test_data')

def test_get_files():
    # all files
    files = rookit.files.get_files2(DATA)
    assert 'some/a.json' in files
    assert 'some/b.json' in files
    assert 'some/c.yml' in files
    assert 'other/a.json' in files
    assert 'other/b.json' in files
    assert 'other/c.yml' in files
    assert 'other/sub_folder/sub_a.json' in files


def test_get_files_extention():
    # yml files
    files = rookit.files.get_files2(DATA, ext='yml')
    assert 'some/a.json' not in files
    assert 'some/b.json' not in files
    assert 'some/c.yml' in files


def test_get_files_folder_blacklist():
    files = rookit.files.get_files2(DATA, folder_blacklist=['other'])
    assert 'some/a.json' in files
    assert 'some/b.json' in files
    assert 'some/c.yml' in files
    assert 'other/a.json' not in files
    assert 'other/b.json' not in files
    assert 'other/c.yml' not in files
    assert 'other/sub_folder/sub_a.json' not in files


def test_get_files_folder_blacklist_subfolder():
    files = rookit.files.get_files2(DATA, folder_blacklist=['*/sub_folder'])
    assert 'some/a.json' in files
    assert 'some/b.json' in files
    assert 'some/c.yml' in files
    assert 'other/a.json' in files
    assert 'other/b.json' in files
    assert 'other/c.yml' in files
    assert 'other/sub_folder/sub_a.json' not in files
