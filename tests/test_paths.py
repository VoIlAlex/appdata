from __future__ import annotations

import os
import shutil
from pathlib import Path

import pytest

import appdata
from appdata import AppDataPaths

from .conftest import folder


class TestInitialization:
    def test_name_defaults_to_cwd(self, cwd: Path, home: Path) -> None:
        assert AppDataPaths().name == "myproject"

    def test_explicit_name(self) -> None:
        assert AppDataPaths(name="some_app").name == "some_app"

    def test_home_defaults_to_user_home(self, home: Path) -> None:
        assert AppDataPaths("x").app_data_path == str(home / folder("x"))

    def test_home_accepts_pathlike(self, tmp_path: Path) -> None:
        paths = AppDataPaths("x", home_folder_path=tmp_path)
        assert paths.app_data_path == os.path.join(str(tmp_path), folder("x"))

    def test_repr(self, app_paths: AppDataPaths) -> None:
        assert "some_app" in repr(app_paths)

    def test_version(self) -> None:
        assert isinstance(appdata.__version__, str)

    @pytest.mark.skipif(os.name == "nt", reason="POSIX hidden folder")
    def test_posix_folder_is_hidden(self, app_paths: AppDataPaths) -> None:
        assert os.path.basename(app_paths.app_data_path) == ".some_app"

    @pytest.mark.skipif(os.name != "nt", reason="Windows folder")
    def test_windows_folder_is_not_hidden(self, app_paths: AppDataPaths) -> None:
        assert os.path.basename(app_paths.app_data_path) == "some_app"


class TestConfigPaths:
    def test_default(self, home: Path) -> None:
        paths = AppDataPaths("some_app")
        assert paths.config_path == str(home / folder("some_app") / "default.ini")

    def test_default_ext(self, home: Path) -> None:
        paths = AppDataPaths("some_app", default_config_ext=".conf")
        assert paths.config_path == str(home / folder("some_app") / "default.conf")

    def test_custom_home(self, tmp_path: Path) -> None:
        paths = AppDataPaths("some_app", default_config_ext="conf", home_folder_path=str(tmp_path))
        assert paths.config_path == os.path.join(str(tmp_path), folder("some_app"), "default.conf")

    @pytest.mark.parametrize("ext", [".some_ext", "some_ext"])
    def test_named(self, app_paths: AppDataPaths, ext: str) -> None:
        assert app_paths.get_config_path(name="cfg", ext=ext) == os.path.join(
            app_paths.app_data_path, "cfg.some_ext"
        )

    def test_empty_name_and_ext(self, app_paths: AppDataPaths) -> None:
        assert app_paths.get_config_path(name="", ext="") == os.path.join(app_paths.app_data_path, "config")

    def test_empty_name(self, app_paths: AppDataPaths) -> None:
        assert app_paths.get_config_path(name="", ext=".conf") == os.path.join(
            app_paths.app_data_path, ".conf"
        )

    def test_create(self, app_paths: AppDataPaths) -> None:
        path = app_paths.get_config_path(name="extra", create=True)
        assert os.path.isfile(path)


class TestLogPaths:
    def test_logs_path(self, app_paths: AppDataPaths) -> None:
        assert app_paths.logs_path == os.path.join(app_paths.app_data_path, "logs")

    def test_custom_logs_folder(self, home: Path) -> None:
        paths = AppDataPaths("some_app", logs_folder_name="some_logs")
        assert paths.logs_path == os.path.join(paths.app_data_path, "some_logs")

    def test_no_logs_folder(self, home: Path) -> None:
        paths = AppDataPaths("some_app", logs_folder_name=None)
        assert paths.logs_path == paths.app_data_path

    def test_log_file_path(self, app_paths: AppDataPaths) -> None:
        assert app_paths.log_file_path == os.path.join(app_paths.logs_path, "some_app.log")

    def test_named_log_file(self, app_paths: AppDataPaths) -> None:
        assert app_paths.get_log_file_path(name="other") == os.path.join(app_paths.logs_path, "other.log")

    def test_log_file_without_app_name(self, app_paths: AppDataPaths, cwd: Path) -> None:
        app_paths.name = ""
        assert app_paths.get_log_file_path() == os.path.join(
            str(app_paths.home_folder_path), folder("myproject"), "logs", "app.log"
        )

    def test_create(self, app_paths: AppDataPaths) -> None:
        assert os.path.isfile(app_paths.get_log_file_path(create=True))


class TestLockPaths:
    def test_lock_file_path(self, app_paths: AppDataPaths) -> None:
        assert app_paths.lock_file_path == os.path.join(app_paths.app_data_path, "locks", "some_app.lock")

    def test_no_locks_folder(self, home: Path) -> None:
        paths = AppDataPaths("some_app", locks_folder_name=None)
        assert paths.locks_path == paths.app_data_path


class TestSetupAndCheck:
    def test_require_setup(self, app_paths: AppDataPaths) -> None:
        assert app_paths.require_setup is True
        app_paths.setup()
        assert app_paths.require_setup is False

    def test_check_before_setup(self, app_paths: AppDataPaths) -> None:
        assert app_paths.check_for_exceptions() is False
        with pytest.raises(RuntimeError, match="setup"):
            app_paths.check_for_exceptions(raise_exceptions=True)

    def test_check_after_setup(self, app_paths: AppDataPaths) -> None:
        app_paths.setup()
        assert app_paths.check_for_exceptions(raise_exceptions=True) is True

    @pytest.mark.parametrize("attr", ["config_path", "log_file_path"])
    def test_missing_file(self, app_paths: AppDataPaths, attr: str) -> None:
        app_paths.setup()
        os.remove(getattr(app_paths, attr))
        assert app_paths.check_for_exceptions() is False
        assert app_paths.require_setup is True

    @pytest.mark.parametrize("attr", ["logs_path", "locks_path"])
    def test_missing_folder(self, app_paths: AppDataPaths, attr: str) -> None:
        app_paths.setup()
        shutil.rmtree(getattr(app_paths, attr))
        assert app_paths.check_for_exceptions() is False

    def test_setup_is_idempotent(self, app_paths: AppDataPaths) -> None:
        app_paths.setup()
        with open(app_paths.config_path, "w") as f:
            f.write("[section]\n")
        app_paths.setup()
        with open(app_paths.config_path) as f:
            assert f.read() == "[section]\n"

    def test_setup_override_removes_locks(self, app_paths: AppDataPaths) -> None:
        app_paths.setup()
        lock_path = app_paths.get_lock_file_path("some_lock")
        Path(lock_path).touch()
        app_paths.setup(override=True)
        assert not os.path.exists(lock_path)
        assert app_paths.check_for_exceptions()


class TestClear:
    def test_clear_keeps_app_data_folder(self, app_paths: AppDataPaths) -> None:
        app_paths.setup()
        user_file = os.path.join(app_paths.app_data_path, "user_data.db")
        Path(user_file).touch()
        app_paths.clear()
        assert os.path.exists(app_paths.app_data_path)
        assert os.path.exists(user_file)
        assert not os.path.exists(app_paths.logs_path)
        assert not os.path.exists(app_paths.config_path)
        assert os.path.isdir(app_paths.locks_path)
        assert os.listdir(app_paths.locks_path) == []

    def test_clear_everything(self, app_paths: AppDataPaths) -> None:
        app_paths.setup()
        app_paths.clear(everything=True)
        assert not os.path.exists(app_paths.app_data_path)

    def test_clear_when_nothing_exists(self, app_paths: AppDataPaths) -> None:
        app_paths.clear()
        app_paths.clear(everything=True)

    def test_clear_without_subfolders_keeps_user_data(self, home: Path) -> None:
        """Regression: clear() used to delete the whole app data folder."""
        paths = AppDataPaths("some_app", logs_folder_name=None, locks_folder_name=None)
        paths.setup()
        user_file = os.path.join(paths.app_data_path, "user_data.db")
        user_dir = os.path.join(paths.app_data_path, "cache")
        Path(user_file).touch()
        os.mkdir(user_dir)
        Path(paths.lock_file_path).touch()

        paths.clear()

        assert os.path.exists(user_file)
        assert os.path.isdir(user_dir)
        assert not os.path.exists(paths.log_file_path)
        assert not os.path.exists(paths.lock_file_path)
        assert not os.path.exists(paths.config_path)
