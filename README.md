# appdata | Application Data Management

## Installation

```bash
pip install appdata
```

## Usage

To manage paths of application data folder there is `AppDataPaths` class:

```python
from appdata import AppDataPaths

paths = AppDataPaths('myapp')
```

To create the application folder tree:

```python
# `verbose` is to log the creation process
paths.setup(verbose=True)
```

There are few paths specified to manage your application data folder:

```python
print(paths.app_name)  # myapp
print(paths.app_data_path)  # (for Linux) /home/<user>/.myapp
print(paths.logs_folder_path)  # (for Linux) /home/<user>/.myapp/logs
print(paths.main_config_path)  # (for Linux) /home/<user>/.myapp/myapp.ini
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

[MIT](LICENSE.md)
