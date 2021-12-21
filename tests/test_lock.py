import os

from appdata import AppDataPaths


class TestLock:
    def test_lock_1(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.setup(override=True)
        lock = app_paths.lock()
        with lock.context():
            pass
        app_paths.clear(everything=True)

    def test_lock_2(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.setup(override=True)
        lock = app_paths.lock()
        lock.acquire()
        lock.release()
        app_paths.clear(everything=True)
