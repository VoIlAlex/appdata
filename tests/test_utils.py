from __future__ import annotations

from pathlib import Path

import pytest

from appdata import get_home_folder, prepare_ext


def test_home_folder() -> None:
    assert get_home_folder() == Path.home().absolute()


def test_home_folder_follows_environment(home: Path) -> None:
    assert get_home_folder() == home


@pytest.mark.parametrize(
    ("ext", "expected"),
    [
        (".ext", ".ext"),
        ("ext", ".ext"),
        ("..ext", ".ext"),
        ("tar.gz", ".tar.gz"),
        ("", ""),
        (".", ""),
        ("..", ""),
        ("...", ""),
        (None, ""),
    ],
)
def test_prepare_ext(ext: str | None, expected: str) -> None:
    assert prepare_ext(ext) == expected
