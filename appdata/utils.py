from functools import lru_cache
from pathlib import Path
from typing import Optional


@lru_cache
def get_home_folder():
    return Path.home().absolute()


@lru_cache
def prepare_ext(ext: Optional[str]):
    if ext and len(ext) != 0:
        while ext.startswith('..'):
            ext = ext[1:]
        if len(ext) == 1 and ext[0] == '.':
            ext = ''

        if len(ext) != 0:
            if ext[0] != '.':
                ext = '.' + ext
    return ext or ''
