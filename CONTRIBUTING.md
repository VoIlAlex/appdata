# Contributing

Thanks for taking the time to contribute! Please read our [Code of Conduct](CODE_OF_CONDUCT.md).

For anything bigger than a small fix, please open an issue first to discuss the change.

## Development setup

```bash
git clone https://github.com/VoIlAlex/appdata.git
cd appdata
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip                       # pip >= 25.1 is needed for --group
python -m pip install -e . --group dev
pre-commit install
```

## Checks

All of these run in CI and must pass:

```bash
pytest --cov              # tests
ruff check .              # lint
ruff format .             # format
mypy                      # type-check
python -m sphinx -W -b html docs docs/_build/html   # docs
```

## Pull requests

1. Add tests for every bug fix or new feature.
2. Update the documentation (`README.md`, `docs/`) when the public API changes.
3. Add an entry under **Unreleased** in [CHANGELOG.md](CHANGELOG.md).

## Releasing (maintainers)

1. Bump `__version__` in `appdata/__init__.py` and move the **Unreleased** changelog
   entries under the new version.
2. Merge to `master`, then create a GitHub Release with the tag `vX.Y.Z`.
3. The `Release` workflow builds the package and publishes it to PyPI using
   [trusted publishing](https://docs.pypi.org/trusted-publishers/).
