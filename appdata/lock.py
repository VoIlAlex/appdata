import os
import time
from contextlib import contextmanager


@contextmanager
def _file_based_lock_context(lock):
    try:
        lock.acquire()
        yield lock
    finally:
        lock.release()


class FileBasedLock:
    def __init__(self, app_paths, name=None):
        self.app_paths = app_paths
        self.name = name

    def acquire(self):
        lock_path = self.app_paths.get_lock_file_path(name=self.name)
        while os.path.exists(lock_path):
            time.sleep(1)
        with open(lock_path, 'w+') as f:
            pass

    def release(self):
        lock_path = self.app_paths.get_lock_file_path(name=self.name)
        if os.path.exists(lock_path):
            os.remove(lock_path)

    def context(self):
        return _file_based_lock_context(self)
