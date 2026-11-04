# Changelog

All notable changes to this project are documented in this file.
The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

## [2.3.0]

### Added
- `FileBasedLock` can be used directly as a context manager (`with app_paths.lock(): ...`).
- Lock `timeout` / `poll_interval` options and `LockTimeoutError`.
- `FileBasedLock.is_held`, `FileBasedLock.is_locked`, `FileBasedLock.path` and `release(force=True)`.
- `AppDataPaths.lock(name=...)` to create named locks.
- `create=True` of `get_config_path()` / `get_log_file_path()` now creates the file
  (the argument was previously accepted but ignored).
- `appdata.__version__`, `__all__`, type hints and a `py.typed` marker (PEP 561).
- `home_folder_path` accepts any path-like object.

### Fixed
- `clear()` deleted the **entire** app data folder (including user files) when
  `logs_folder_name` was `None`, and crashed when `locks_folder_name` was `None`.
- Lock acquisition had a race condition: two processes could acquire the lock at the
  same time. The lock file is now created atomically.
- `release()` no longer removes a lock held by another process.
- The lock no longer fails when the locks folder does not exist yet.
- The app data folder is now hidden (`~/.name`) on every POSIX platform (e.g. FreeBSD),
  not only on Linux and macOS.
- `get_home_folder()` is no longer cached, so it follows changes of the home directory.
- The `tests` package is no longer installed into `site-packages`.
- Invalid configuration raises `ValueError` instead of `AssertionError`.

### Changed
- Packaging moved from `setup.py` (which relied on the removed `distutils`) to
  `pyproject.toml`.
- Minimum supported Python version is 3.9; tested on 3.9–3.14 on Linux, macOS and Windows.
- Releases are published to PyPI from GitHub Releases via trusted publishing.

## [2.2.1] and earlier

See the [commit history](https://github.com/VoIlAlex/appdata/commits/master).

[Unreleased]: https://github.com/VoIlAlex/appdata/compare/v2.3.0...HEAD
[2.3.0]: https://github.com/VoIlAlex/appdata/releases/tag/v2.3.0
