from __future__ import annotations

import os
import threading
import time

import pytest

from appdata import AppDataPaths, FileBasedLock, LockTimeoutError


def test_context_manager(app_paths: AppDataPaths) -> None:
    app_paths.setup()
    lock = app_paths.lock()
    with lock as held:
        assert held is lock
        assert lock.is_held
        assert lock.is_locked
        assert os.path.exists(app_paths.lock_file_path)
    assert not lock.is_held
    assert not lock.is_locked


def test_legacy_context(app_paths: AppDataPaths) -> None:
    lock = app_paths.lock()
    with lock.context():
        assert lock.is_locked
    assert not lock.is_locked


def test_released_on_exception(app_paths: AppDataPaths) -> None:
    lock = app_paths.lock()
    with pytest.raises(ValueError, match="boom"), lock:
        raise ValueError("boom")
    assert not lock.is_locked


def test_acquire_release(app_paths: AppDataPaths) -> None:
    lock = app_paths.lock()
    lock.acquire()
    with open(lock.path) as f:
        assert f.read() == str(os.getpid())
    lock.release()
    lock.release()  # idempotent
    assert not lock.is_locked


def test_acquire_without_setup_creates_folder(app_paths: AppDataPaths) -> None:
    with app_paths.lock():
        assert os.path.isdir(app_paths.locks_path)


def test_named_locks_are_independent(app_paths: AppDataPaths) -> None:
    with app_paths.lock("a"), app_paths.lock("b", timeout=0):
        pass


def test_timeout(app_paths: AppDataPaths) -> None:
    with app_paths.lock():
        other = app_paths.lock(poll_interval=0.01)
        with pytest.raises(LockTimeoutError):
            other.acquire(timeout=0.05)
        assert not other.is_held
    other.acquire(timeout=0)
    other.release()


def test_release_does_not_steal_foreign_lock(app_paths: AppDataPaths) -> None:
    with app_paths.lock():
        other = app_paths.lock()
        other.release()
        assert other.is_locked
        other.release(force=True)
        assert not other.is_locked


def test_not_reentrant(app_paths: AppDataPaths) -> None:
    with app_paths.lock() as lock, pytest.raises(RuntimeError):
        lock.acquire()


def test_invalid_poll_interval(app_paths: AppDataPaths) -> None:
    with pytest.raises(ValueError, match="poll_interval"):
        FileBasedLock(app_paths, poll_interval=0)


def test_mutual_exclusion(app_paths: AppDataPaths) -> None:
    inside = 0
    max_inside = 0
    guard = threading.Lock()

    def worker() -> None:
        nonlocal inside, max_inside
        with app_paths.lock(poll_interval=0.001):
            with guard:
                inside += 1
                max_inside = max(max_inside, inside)
            time.sleep(0.005)
            with guard:
                inside -= 1

    threads = [threading.Thread(target=worker) for _ in range(8)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    assert max_inside == 1
