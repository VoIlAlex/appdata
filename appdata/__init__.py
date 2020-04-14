import configparser
import os
import sys
from loguru import logger


class AppDataPaths:
    def __init__(self, app_name: str, config_ext: str = 'ini'):
        self.app_name = app_name
        self.app_data_path = None
        if sys.platform == 'linux':
            self.app_data_path = os.path.join(
                os.getenv('HOME'), f'.{app_name}')
        else:
            self.app_data_path = os.path.join(
                os.getenv('HOMEPATH'), f'.{app_name}')
        self.logs_folder_path = os.path.join(self.app_data_path, 'logs')
        self.main_config_path = os.path.join(self.app_data_path, f'{app_name}.config')

    def setup(self, verbose: bool = False):
        """Setup app data folder. Create all the missing folders and files.
        
        Keyword Arguments:
            verbose {bool} -- whether to log the process of setting up (default: {False})
        """
        # Create app data path
        if verbose:
            logger.info('Creating the data folder...')
        if not os.path.exists(self.app_data_path):
            os.makedirs(self.app_data_path)
        elif verbose:
            logger.warning('Application data folder already exists.')

        # Create logs folder
        if verbose:
            logger.info('Creating the logs folder...')
        if not os.path.exists(self.logs_folder_path):
            os.makedirs(self.logs_folder_path)
        elif verbose:
            logger.warning('Logs folder already exists.')


        # Create config file
        if verbose:
            logger.info('Creating the main config file...')
        if not os.path.exists(self.main_config_path):
            open(self.main_config_path, 'w+').close()
        elif verbose:
            logger.warning('Main config file already exists.')

    def join(self, *paths) -> str:
        """Join paths with path of the app data folder.
        
        Returns:
            str -- joint paths.
        """
        return os.path.join(self.app_data_path, *paths)
