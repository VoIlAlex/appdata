from __future__ import annotations

import os
from pathlib import Path

import pytest

from appdata import AppDataPaths


def folder(name: str) -> str:
    """Expected app data folder name for the current platform."""
    return name if os.name == "nt" else f".{name}"


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fake home directory so tests never touch the real one."""
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setattr(Path, "home", classmethod(lambda cls: home))
    return home


@pytest.fixture
def cwd(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Run the test from a working directory named ``myproject``."""
    path = tmp_path / "myproject"
    path.mkdir()
    monkeypatch.chdir(path)
    return path


@pytest.fixture
def app_paths(home: Path) -> AppDataPaths:
    return AppDataPaths(name="some_app", home_folder_path=home)
