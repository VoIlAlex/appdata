"""Small helpers used by :mod:`appdata`."""

from __future__ import annotations

from pathlib import Path

__all__ = ["get_home_folder", "prepare_ext"]


def get_home_folder() -> Path:
    """Return the absolute path of the current user's home directory."""
    return Path.home().absolute()


def prepare_ext(ext: str | None) -> str:
    """Normalize a file extension.

    The result is either an empty string or a string that starts with exactly
    one dot::

        >>> prepare_ext("ini")
        '.ini'
        >>> prepare_ext("..ini")
        '.ini'
        >>> prepare_ext(".")
        ''
        >>> prepare_ext(None)
        ''
    """
    if not ext:
        return ""
    ext = "." + ext.lstrip(".")
    return "" if ext == "." else ext
