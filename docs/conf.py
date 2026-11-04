"""Sphinx configuration."""

from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.abspath(".."))

from appdata import __version__

project = "appdata"
author = "Ilya Vouk"
copyright = f"2020, {author}"
version = release = __version__

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
]
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autoclass_content = "both"
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}

exclude_patterns = ["_build"]
html_theme = "furo"
html_title = f"appdata {release}"
