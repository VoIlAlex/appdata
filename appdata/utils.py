from functools import cache
from pathlib import Path
from typing import Optional


@cache
def get_home_folder():
    return Path.home().absolute()


@cache
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
