import os
import pytest
from agents.tools.file_access import list_files


def test_list_files_existing_directory(tmp_path):
    # Create a mix of a file and a directory to ensure both are listed
    (tmp_path / "a.txt").write_text("hello")
    (tmp_path / "dir").mkdir()
    (tmp_path / "space name.txt").write_text("x")

    entries = list_files(str(tmp_path))

    assert isinstance(entries, list)
    assert set(entries) == {"a.txt", "dir", "space name.txt"}


def test_list_files_non_existent_directory():
    non_exist = "nonexistent_dir_123456789"
    res = list_files(non_exist)
    assert res == [f"Could not find directory {non_exist}"]


def test_list_files_empty_path_uses_current_directory(tmp_path, monkeypatch):
    # Prepare a couple of entries in the temp directory
    (tmp_path / "f1.txt").write_text("1")
    (tmp_path / "sub").mkdir()

    # Change current working directory to the temp path
    monkeypatch.chdir(tmp_path)

    res = list_files("")

    assert isinstance(res, list)
    assert set(res) == {"f1.txt", "sub"}
