import os
import shutil
from appdata import AppDataPaths
from pathlib import Path


class TestPaths:
    def test_paths_initialization_1(self):
        app = AppDataPaths()
        assert app.name == 'appdata'

    def test_paths_initialization_2(self):
        app = AppDataPaths(
            name='some_app'
        )
        assert app.name == 'some_app'

    def test_require_setup_1(self):
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext='.conf',
            home_folder_path=os.getcwd()
        )
        require_setup = not os.path.exists(app_paths.home_folder_path) \
                        or not os.path.exists(app_paths.config_path)
        return app_paths.require_setup == require_setup


class TestConfigPaths:
    def test_config_path_1(self):
        app_paths = AppDataPaths()
        assert app_paths.config_path == os.path.join(
            Path.home(),
            '.appdata',
            'default' + AppDataPaths.DEFAULT_EXT
        )

    def test_config_path_2(self):
        app_paths = AppDataPaths(default_confing_ext='.conf')
        assert app_paths.config_path == os.path.join(
            Path.home(),
            '.appdata',
            'default.conf'
        )

    def test_config_path_3(self):
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext='.conf'
        )
        assert app_paths.config_path == os.path.join(
            Path.home(),
            '.some_app',
            'default.conf'
        )

    def test_config_path_4(self):
        home_folder_path = os.getcwd()
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext='.conf',
            home_folder_path=home_folder_path
        )
        assert app_paths.config_path == os.path.join(
            home_folder_path,
            '.some_app',
            'default.conf'
        )

    def test_config_path_5(self):
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext='.conf'
        )
        config_path = app_paths.get_config_path(
            name='some_config',
            ext='.some_ext'
        )
        assert config_path == os.path.join(
            Path.home(),
            '.some_app',
            'some_config.some_ext'
        )

    def test_config_path_6(self):
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext='.conf'
        )
        config_path = app_paths.get_config_path(
            name='some_config',
            ext='some_ext'
        )
        assert config_path == os.path.join(
            Path.home(),
            '.some_app',
            'some_config.some_ext'
        )

    def test_config_path_7(self):
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext=None
        )
        config_path = app_paths.get_config_path(
            name='',
            ext=''
        )
        assert config_path == os.path.join(
            Path.home(),
            '.some_app',
            'config'
        )

    def test_config_path_8(self):
        app_paths = AppDataPaths(
            name='some_app',
            default_confing_ext=None
        )
        config_path = app_paths.get_config_path(
            name='',
            ext='.conf'
        )
        assert config_path == os.path.join(
            Path.home(),
            '.some_app',
            '.conf'
        )

class TestLogPaths:
    def test_logs_path_1(self):
        app_paths = AppDataPaths()
        assert app_paths.logs_path == os.path.join(
            Path.home(),
            '.appdata',
            'logs',
        )

    def test_logs_path_2(self):
        app_paths = AppDataPaths(logs_folder_name='some_logs')
        assert app_paths.logs_path == os.path.join(
            Path.home(),
            '.appdata',
            'some_logs',
        )

    def test_logs_path_3(self):
        app_paths = AppDataPaths(logs_folder_name=None)
        assert app_paths.logs_path == os.path.join(
            Path.home(),
            '.appdata',
        )

    def test_log_file_path_4(self):
        app_paths = AppDataPaths()
        assert app_paths.log_file_path == os.path.join(
            Path.home(),
            '.appdata',
            'logs',
            'appdata.log'
        )

    def test_log_file_path_5(self):
        app_paths = AppDataPaths()
        assert app_paths.get_log_file_path(name='something') == os.path.join(
            Path.home(),
            '.appdata',
            'logs',
            'something.log'
        )

    def test_log_file_path_6(self):
        app_paths = AppDataPaths()
        app_paths.name = ''
        assert app_paths.get_log_file_path() == os.path.join(
            Path.home(),
            '.appdata',
            'logs',
            'app.log'
        )


class TestPathsUtils:
    def test_check_for_exceptions_1(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.clear(everything=True)
        assert app_paths.check_for_exceptions() is False

    def test_check_for_exceptions_2(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.clear(everything=True)
        assert app_paths.check_for_exceptions(raise_exceptions=False) is False

    def test_check_for_exceptions_3(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.clear(everything=True)
        try:
            app_paths.check_for_exceptions(raise_exceptions=True)
        except Exception:
            return
        assert False

    def test_check_for_exceptions_4(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.setup()
        assert app_paths.check_for_exceptions(raise_exceptions=False)
        app_paths.clear(everything=True)

    def test_check_for_exceptions_5(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.setup()
        os.remove(app_paths.config_path)
        assert not app_paths.check_for_exceptions(raise_exceptions=False)
        app_paths.clear(everything=True)

    def test_check_for_exceptions_6(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.setup()
        os.remove(app_paths.log_file_path)
        assert not app_paths.check_for_exceptions(raise_exceptions=False)
        app_paths.clear(everything=True)

    def test_check_for_exceptions_7(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.setup()
        shutil.rmtree(app_paths.logs_path)
        assert not app_paths.check_for_exceptions(raise_exceptions=False)
        app_paths.clear(everything=True)

    def test_setup_1(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.clear(everything=True)
        assert app_paths.require_setup is True
        app_paths.setup()
        assert app_paths.require_setup is False
        app_paths.clear(everything=True)

    def test_clear_1(self):
        """
        Simple clear clears only default generated files.
        But app data folder and other content stays in place.
        """
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.clear(everything=True)
        assert not os.path.exists(app_paths.app_data_path)
        app_paths.setup()
        assert os.path.exists(app_paths.app_data_path)
        assert os.path.exists(app_paths.logs_path)
        assert os.path.exists(app_paths.config_path)
        assert os.path.exists(app_paths.log_file_path)
        app_paths.clear()
        assert os.path.exists(app_paths.app_data_path)
        assert not os.path.exists(app_paths.logs_path)
        assert not os.path.exists(app_paths.config_path)
        assert not os.path.exists(app_paths.log_file_path)
        app_paths.clear(everything=True)

    def test_clear_2(self):
        app_paths = AppDataPaths(
            home_folder_path=os.getcwd()
        )
        app_paths.clear(everything=True)
        assert not os.path.exists(app_paths.app_data_path)
        app_paths.setup()
        assert os.path.exists(app_paths.app_data_path)
        app_paths.clear(everything=True)
        assert not os.path.exists(app_paths.app_data_path)
