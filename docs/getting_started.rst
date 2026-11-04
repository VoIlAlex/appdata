Getting started
===============

Installation
------------

.. code-block:: none

    pip install appdata

``appdata`` has no dependencies and supports Python 3.9+.

Basic usage
-----------

The main class of the package is :class:`~appdata.AppDataPaths`:

.. code-block:: python

    from appdata import AppDataPaths

    app_paths = AppDataPaths("myapp")
    app_paths.setup()

If ``name`` is omitted, the name of the current working directory is used.

``setup()`` creates every missing file and folder; it never overwrites
existing files. To check whether ``setup()`` is required:

.. code-block:: python

    app_paths.require_setup          # True / False
    app_paths.check_for_exceptions() # True / False, or raise_exceptions=True

Folder location
---------------

The app data folder is created in the user's home directory:

============================  =============================
Platform                      ``app_paths.app_data_path``
============================  =============================
Linux, macOS, other POSIX     ``~/.myapp``
Windows                       ``%USERPROFILE%\myapp``
============================  =============================

Use ``home_folder_path=...`` to place it somewhere else.

Layout created by ``setup()``:

.. code-block:: none

    ~/.myapp/
        default.ini        app_paths.config_path
        logs/              app_paths.logs_path
            myapp.log      app_paths.log_file_path
        locks/             app_paths.locks_path

Every name can be customized:

.. code-block:: python

    AppDataPaths(
        "myapp",
        default_config_ext=".toml",   # default.toml
        logs_folder_name="log",       # None stores logs in the app data folder
        locks_folder_name=None,       # lock files in the app data folder
        home_folder_path="/srv/data",
    )

Config and log files
--------------------

.. code-block:: python

    app_paths.config_path                                   # default config
    app_paths.get_config_path(name="secrets", ext=".json")  # another config
    app_paths.get_config_path(name="cache", create=True)    # ...and create it

    app_paths.log_file_path                                 # default log file
    app_paths.get_log_file_path(name="worker", create=True)

Locks
-----

:meth:`~appdata.AppDataPaths.lock` returns a cross-process
:class:`~appdata.lock.FileBasedLock`:

.. code-block:: python

    from appdata import LockTimeoutError

    with app_paths.lock():
        ...  # only one process at a time gets here

    try:
        with app_paths.lock("db", timeout=5):
            ...
    except LockTimeoutError:
        print("Another process is using the database")

The lock file is created atomically, so it is safe to use from several
processes. If a process is killed while holding the lock, remove the stale
lock with ``app_paths.lock().release(force=True)``.

Cleaning up
-----------

.. code-block:: python

    app_paths.clear()                 # default config, logs and lock files
    app_paths.clear(everything=True)  # the whole app data folder

``clear()`` never removes other files you have stored in the app data folder.
