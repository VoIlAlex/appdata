# appdata

[![PyPI](https://img.shields.io/pypi/v/appdata)](https://pypi.org/project/appdata/)
[![Python versions](https://img.shields.io/pypi/pyversions/appdata)](https://pypi.org/project/appdata/)
[![CI](https://github.com/VoIlAlex/appdata/actions/workflows/ci.yml/badge.svg)](https://github.com/VoIlAlex/appdata/actions/workflows/ci.yml)
[![Coverage Status](https://coveralls.io/repos/github/VoIlAlex/appdata/badge.svg?branch=master)](https://coveralls.io/github/VoIlAlex/appdata?branch=master)
[![Documentation](https://img.shields.io/readthedocs/appdata)](https://appdata.readthedocs.io/en/latest/)
[![License](https://img.shields.io/github/license/VoIlAlex/appdata)](https://github.com/VoIlAlex/appdata/blob/master/LICENSE.md)
[![Downloads](https://static.pepy.tech/badge/appdata)](https://pepy.tech/project/appdata)

**appdata** is a small, dependency-free, fully typed library to manage the data folder of
your application — config files, log files and cross-process file locks — on Linux, macOS
and Windows.

## Installation

```bash
pip install appdata
```

Requires Python 3.9+.

## Usage

```python
from appdata import AppDataPaths

app_paths = AppDataPaths("myapp")  # Name is optional; defaults to the CWD folder name.
app_paths.setup()                  # Creates missing files and folders, never overwrites.
```

```python
app_paths.app_data_path  # ~/.myapp               (%USERPROFILE%\myapp on Windows)
app_paths.config_path    # ~/.myapp/default.ini
app_paths.logs_path      # ~/.myapp/logs
app_paths.log_file_path  # ~/.myapp/logs/myapp.log
app_paths.locks_path     # ~/.myapp/locks

app_paths.get_config_path(name="secrets", ext=".json", create=True)
app_paths.get_log_file_path(name="worker")
```

Allow only one process at a time into a critical section:

```python
with app_paths.lock(timeout=10):  # raises appdata.LockTimeoutError on timeout
    ...
```

Clean up:

```python
app_paths.clear()                 # default config, logs and lock files
app_paths.clear(everything=True)  # the whole app data folder
```

Every name and location can be customized; see the
[documentation](https://appdata.readthedocs.io/).

## Contributing

Contributions are welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE.md)
