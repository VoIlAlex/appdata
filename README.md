# appdata | Application Data Management

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
