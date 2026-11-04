"""A simple cross-process lock backed by a file in the app data folder."""

from __future__ import annotations

import os
import time
from contextlib import AbstractContextManager, contextmanager, suppress
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterator
    from types import TracebackType

    from appdata import AppDataPaths

__all__ = ["FileBasedLock", "LockTimeoutError"]


class LockTimeoutError(TimeoutError):
    """Raised when a lock could not be acquired within the given timeout."""


class FileBasedLock:
    """An exclusive, cross-process lock implemented with a lock file.

    The lock file is created atomically (``O_CREAT | O_EXCL``), so two
    processes can never both believe they hold the lock. The lock is *not*
    re-entrant.

    It can be used as a context manager::

        with app_paths.lock():
            ...

    .. note::
        If a process dies while holding the lock, the lock file stays on disk
        and has to be removed with ``release(force=True)``.
    """

    def __init__(
        self,
        app_paths: AppDataPaths,
        name: str | None = None,
        *,
        timeout: float | None = None,
        poll_interval: float = 0.1,
    ) -> None:
        """
        :param app_paths: :class:`~appdata.AppDataPaths` the lock belongs to.
        :param name: name of the lock. Defaults to the application name.
        :param timeout: default number of seconds :meth:`acquire` waits
            before raising :class:`LockTimeoutError`. ``None`` waits forever.
        :param poll_interval: seconds to sleep between acquisition attempts.
        """
        if poll_interval <= 0:
            raise ValueError("poll_interval must be positive")
        self.app_paths = app_paths
        self.name = name
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._held = False

    @property
    def path(self) -> str:
        """Path of the lock file."""
        return self.app_paths.get_lock_file_path(name=self.name)

    @property
    def is_held(self) -> bool:
        """Whether this lock object currently holds the lock."""
        return self._held

    @property
    def is_locked(self) -> bool:
        """Whether the lock is currently held by anyone."""
        return os.path.exists(self.path)

    def acquire(self, timeout: float | None = None) -> None:
        """Block until the lock is acquired.

        :param timeout: seconds to wait; overrides the timeout given to the
            constructor. ``None`` uses the constructor value.
        :raises LockTimeoutError: if the lock was not acquired in time.
        :raises RuntimeError: if this object already holds the lock.
        """
        if self._held:
            raise RuntimeError(f"Lock {self.path!r} is already held by this object")
        if timeout is None:
            timeout = self.timeout

        lock_path = self.path
        os.makedirs(os.path.dirname(lock_path), exist_ok=True)
        deadline = None if timeout is None else time.monotonic() + timeout

        while True:
            try:
                fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o644)
            except FileExistsError:
                if deadline is not None and time.monotonic() >= deadline:
                    raise LockTimeoutError(
                        f"Could not acquire lock {lock_path!r} within {timeout} seconds"
                    ) from None
                time.sleep(self.poll_interval)
                continue
            with os.fdopen(fd, "w") as f:
                f.write(str(os.getpid()))
            self._held = True
            return

    def release(self, force: bool = False) -> None:
        """Release the lock.

        :param force: remove the lock file even if this object does not hold
            the lock (e.g. to clean up after a crashed process).
        """
        if not (self._held or force):
            return
        with suppress(FileNotFoundError):
            os.remove(self.path)
        self._held = False

    def context(self) -> AbstractContextManager[FileBasedLock]:
        """Return a context manager that holds the lock (kept for backward compatibility)."""
        return _file_based_lock_context(self)

    def __enter__(self) -> FileBasedLock:
        self.acquire()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.release()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(path={self.path!r}, held={self._held})"


@contextmanager
def _file_based_lock_context(lock: FileBasedLock) -> Iterator[FileBasedLock]:
    lock.acquire()
    try:
        yield lock
    finally:
        lock.release()
