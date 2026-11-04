"""Manage the paths of an application's data folder.

Example::

    from appdata import AppDataPaths

    app_paths = AppDataPaths("myapp")
    app_paths.setup()
    print(app_paths.config_path)
"""

from __future__ import annotations

import os
import shutil
from typing import Any

from appdata.lock import FileBasedLock, LockTimeoutError
from appdata.utils import get_home_folder, prepare_ext

__version__ = "2.3.0"

__all__ = [
    "AppDataPaths",
    "FileBasedLock",
    "LockTimeoutError",
    "__version__",
    "get_home_folder",
    "prepare_ext",
]

_SETUP_HINT = "Run setup() to initialize the required files."


class AppDataPaths:
    """Paths of an application data folder.

    The application data folder is located in the user's home directory. On
    POSIX systems (Linux, macOS, BSD, ...) it is hidden, i.e. ``~/.<name>``;
    on Windows it is ``%USERPROFILE%\\<name>``.

    Layout created by :meth:`setup`::

        <app_data_path>/
            default.ini          # config_path
            logs/                # logs_path
                <name>.log       # log_file_path
            locks/               # locks_path
    """

    DEFAULT_EXT = ".ini"
    DEFAULT_CONFIG_NAME = "default"
    DEFAULT_LOG_FILE_NAME = "app"
    DEFAULT_LOCK_FILE_NAME = "lock"

    def __init__(
        self,
        name: str | None = None,
        default_config_ext: str | None = None,
        logs_folder_name: str | None = "logs",
        locks_folder_name: str | None = "locks",
        home_folder_path: str | os.PathLike[str] | None = None,
    ) -> None:
        """
        :param name: name of the application. Defaults to the name of the
            current working directory.
        :param default_config_ext: extension of the default config file.
            Defaults to :attr:`DEFAULT_EXT` (``.ini``).
        :param logs_folder_name: name of the logs sub-folder. If falsy, logs
            are stored directly in the app data folder.
        :param locks_folder_name: name of the locks sub-folder. If falsy,
            lock files are stored directly in the app data folder.
        :param home_folder_path: folder in which the app data folder is
            created. Defaults to the user's home directory.
        """
        self.name = name if name else self.default_name
        self.default_config_ext = default_config_ext
        self.home_folder_path = os.fspath(home_folder_path) if home_folder_path else get_home_folder()
        self.logs_folder_name = logs_folder_name
        self.locks_folder_name = locks_folder_name

        if not self.name:
            raise ValueError("Application name could not be determined; pass `name` explicitly.")

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name={self.name!r}, app_data_path={self.app_data_path!r})"

    # ------------------------------------------------------------------ paths

    def get_config_path(
        self,
        name: str | None = None,
        ext: str | None = None,
        create: bool = False,
    ) -> str:
        """Return the path of a config file in the app data folder.

        :param name: config file name without extension. Defaults to
            :attr:`DEFAULT_CONFIG_NAME` (``default``).
        :param ext: file extension. Defaults to ``default_config_ext``.
        :param create: create the file (and its parent folders) if it does
            not exist.
        :return: path to the config file.
        """
        if ext is None:
            ext = self.default_config_ext if self.default_config_ext is not None else self.DEFAULT_EXT
        ext = prepare_ext(ext)
        name = name if name is not None else self.DEFAULT_CONFIG_NAME

        full_name = name + ext if name else ext or "config"

        path = os.path.join(self.app_data_path, full_name)
        if create:
            _touch(path)
        return path

    def get_log_file_path(self, name: str | None = None, create: bool = False) -> str:
        """Return the path of a log file in the logs folder.

        :param name: log file name without extension. Defaults to the
            application name.
        :param create: create the file (and its parent folders) if it does
            not exist.
        """
        name = name or self.name or self.DEFAULT_LOG_FILE_NAME
        path = os.path.join(self.logs_path, name + ".log")
        if create:
            _touch(path)
        return path

    def get_lock_file_path(self, name: str | None = None) -> str:
        """Return the path of a lock file in the locks folder.

        :param name: lock name. Defaults to the application name.
        """
        name = name or self.name or self.DEFAULT_LOCK_FILE_NAME
        return os.path.join(self.locks_path, name + ".lock")

    @property
    def default_name(self) -> str:
        """Name of the current working directory."""
        return os.path.basename(os.getcwd())

    @property
    def app_data_path(self) -> str:
        """Root folder of the application data."""
        name = self.name or self.default_name
        folder_name = name if os.name == "nt" else f".{name}"
        return os.path.join(self.home_folder_path, folder_name)

    @property
    def logs_path(self) -> str:
        """Folder containing the log files."""
        if self.logs_folder_name:
            return os.path.join(self.app_data_path, self.logs_folder_name)
        return self.app_data_path

    @property
    def locks_path(self) -> str:
        """Folder containing the lock files."""
        if self.locks_folder_name:
            return os.path.join(self.app_data_path, self.locks_folder_name)
        return self.app_data_path

    @property
    def config_path(self) -> str:
        """Path of the default config file."""
        return self.get_config_path()

    @property
    def log_file_path(self) -> str:
        """Path of the default log file."""
        return self.get_log_file_path()

    @property
    def lock_file_path(self) -> str:
        """Path of the default lock file."""
        return self.get_lock_file_path()

    # -------------------------------------------------------------- lifecycle

    def _missing(self) -> str | None:
        """Return a description of the first missing required path, if any."""
        required = (
            (self.app_data_path, "App data folder"),
            (self.config_path, "Config file"),
            (self.logs_path, "Logs folder"),
            (self.log_file_path, "Default log file"),
            (self.locks_path, "Locks folder"),
        )
        for path, description in required:
            if not os.path.exists(path):
                return f"{description} {path!r} does not exist. {_SETUP_HINT}"
        return None

    @property
    def require_setup(self) -> bool:
        """Whether :meth:`setup` has to be called to create missing files."""
        return self._missing() is not None

    def check_for_exceptions(self, raise_exceptions: bool = False) -> bool:
        """Check that all the required files and folders exist.

        :param raise_exceptions: raise :class:`RuntimeError` describing the
            first missing path instead of returning ``False``.
        :return: ``True`` if everything exists.
        """
        missing = self._missing()
        if missing is None:
            return True
        if raise_exceptions:
            raise RuntimeError(missing)
        return False

    def setup(self, override: bool = False) -> None:
        """Create the app data folder tree.

        :param override: call :meth:`clear` first, recreating the default
            config file, the logs folder and removing the lock files.
        """
        if override:
            self.clear()
        os.makedirs(self.app_data_path, exist_ok=True)
        os.makedirs(self.logs_path, exist_ok=True)
        os.makedirs(self.locks_path, exist_ok=True)
        _touch(self.config_path)
        _touch(self.log_file_path)

    def clear(self, everything: bool = False) -> None:
        """Remove the files created by :meth:`setup`.

        :param everything: remove the whole app data folder, including any
            other files stored in it. Otherwise only the default config file,
            the logs and the lock files are removed.
        """
        app_data_path = self.app_data_path
        if everything:
            if os.path.exists(app_data_path):
                shutil.rmtree(app_data_path)
            return

        _remove_file(self.config_path)

        logs_path = self.logs_path
        if os.path.normpath(logs_path) == os.path.normpath(app_data_path):
            # Logs share the app data folder: never remove the folder itself.
            _remove_matching(logs_path, ".log")
        elif os.path.isdir(logs_path):
            shutil.rmtree(logs_path)
        else:
            _remove_file(logs_path)

        locks_path = self.locks_path
        if os.path.normpath(locks_path) == os.path.normpath(app_data_path):
            _remove_matching(locks_path, ".lock")
        elif os.path.isdir(locks_path):
            for entry in os.listdir(locks_path):
                _remove_file(os.path.join(locks_path, entry))
        else:
            _remove_file(locks_path)

    def lock(self, name: str | None = None, **kwargs: Any) -> FileBasedLock:
        """Return a :class:`~appdata.lock.FileBasedLock` stored in the locks folder.

        :param name: lock name. Defaults to the application name.
        :param kwargs: extra arguments for :class:`~appdata.lock.FileBasedLock`
            (``timeout``, ``poll_interval``).
        """
        return FileBasedLock(self, name=name, **kwargs)


def _touch(path: str) -> None:
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if not os.path.exists(path):
        with open(path, "a"):
            pass


def _remove_file(path: str) -> None:
    if os.path.isfile(path) or os.path.islink(path):
        os.remove(path)


def _remove_matching(folder: str, suffix: str) -> None:
    if not os.path.isdir(folder):
        return
    for entry in os.listdir(folder):
        if entry.endswith(suffix):
            _remove_file(os.path.join(folder, entry))
