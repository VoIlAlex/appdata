# appdata | Application Data Management

[![Coverage Status](https://coveralls.io/repos/github/VoIlAlex/appdata/badge.svg?branch=master&)](https://coveralls.io/github/VoIlAlex/appdata?branch=master)
[![PyPI release](https://img.shields.io/pypi/v/appdata)](https://pypi.org/project/appdata/)
![Build status](https://github.com/VoIlAlex/appdata/actions/workflows/publish-to-pypi.yml/badge.svg)
[![Documentation](https://img.shields.io/readthedocs/appdata)](https://appdata.readthedocs.io/en/latest/)


[![Maintainability](https://api.codeclimate.com/v1/badges/b909411d678ef3500d92/maintainability)](https://codeclimate.com/github/VoIlAlex/appdata/maintainability)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License](https://img.shields.io/github/license/VoIlAlex/appdata)](https://github.com/VoIlAlex/appdata/blob/master/LICENSE.md)
[![Downloads](https://static.pepy.tech/personalized-badge/appdata?period=total&units=international_system&left_color=grey&right_color=green&left_text=Downloads)](https://pepy.tech/project/appdata)


[![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg)
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![macOS](https://svgshare.com/i/ZjP.svg)](https://svgshare.com/i/ZjP.svg)

## Installation

```bash
pip install appdata
```

## Documentation

The detailed documentation you can find on [appdata.readthedocs.io](https://appdata.readthedocs.io/en/latest/index.html).

## Usage

To manage paths of application data folder there is `AppDataPaths` class:

```python
from appdata import AppDataPaths

app_paths = AppDataPaths('myapp')  # Name is optional. By default CWD folder name is used.
```

To create the application folder tree:

```python
paths.setup()
```

There are few paths specified to manage your application data folder:

```python
print(app_paths.name)  # myapp
print(app_paths.app_data_path)  # (for Linux) /home/<user>/.myapp
print(app_paths.logs_path)  # (for Linux) /home/<user>/.myapp/logs
print(app_paths.config_path)  # (for Linux) /home/<user>/.myapp/myapp.ini
print(app_paths.log_file_path)  # (for Linux) /home/<user>/.myapp/logs/myapp.log
```

Every path could be customized. See options [here](https://appdata.readthedocs.io/).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[MIT](LICENSE.md)
