import os
from pathlib import Path
import pytest
from tools.file_access import read_file, edit_file, list_files


def test_read_file_reads_content(tmp_path):
    p = tmp_path / 'sample.txt'
    p.write_text('Hello world')
    assert read_file(str(p)) == 'Hello world'


def test_read_file_nonexistent(tmp_path):
    p = tmp_path / 'no_such_file.txt'
    assert read_file(str(p)) == f'Could not find file {str(p)} in workspace'


def test_read_file_empty_path_returns_empty():
    assert read_file('') == ''


def test_edit_file_create_new_file(tmp_path):
    path = tmp_path / 'newfile.txt'
    res = edit_file(str(path), old_str='old', new_str='content')
    assert res.startswith('Created new file')
    assert path.exists()
    assert path.read_text() == 'content'


def test_edit_file_append_when_old_empty(tmp_path):
    path = tmp_path / 'append.txt'
    path.write_text('Line1')
    res = edit_file(str(path), old_str='', new_str='Appended')
    assert res.startswith("Appended 'Appended'")
    assert path.read_text() == 'Line1\nAppended'


def test_edit_file_replace_once(tmp_path):
    path = tmp_path / 'replace.txt'
    path.write_text('Start old End')
    res = edit_file(str(path), old_str='old', new_str='new')
    assert res.startswith("Replaced 'old'")
    assert path.read_text() == 'Start new End'


def test_edit_file_old_not_found(tmp_path):
    path = tmp_path / 'nofind.txt'
    path.write_text('abcdef')
    res = edit_file(str(path), old_str='xyz', new_str='123')
    assert res == 'Edit failed: old_str not found in file.'
    assert path.read_text() == 'abcdef'


def test_edit_file_old_not_unique(tmp_path):
    path = tmp_path / 'dups.txt'
    path.write_text('dup dup')
    res = edit_file(str(path), old_str='dup', new_str='X')
    assert res == 'Edit failed: old_str found 2 times in file, must be unique.'
    assert path.read_text() == 'dup dup'


def test_list_files_existing_and_nonexistent(tmp_path):
    f = tmp_path / 'a.txt'
    f.write_text('a')
    d = tmp_path / 'dir'
    d.mkdir()
    f2 = tmp_path / 'b.txt'
    f2.touch()
    result = list_files(str(tmp_path))
    expected = set(os.listdir(tmp_path))
    assert set(result) == expected


def test_list_files_nonexistent(tmp_path):
    p = tmp_path / 'no_such_dir'
    res = list_files(str(p))
    assert res == [f'Could not find directory {str(p)}']
