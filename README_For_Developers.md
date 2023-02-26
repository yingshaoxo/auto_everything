# auto_everything

Linux/MacOS automation

## Install poetry

```
curl -sSL https://install.python-poetry.org | python3
```

## Get into the shell

```bash
poetry shell
```

## Get virtual env info

```bash
poetry env info
```

## add a package

```bash
poetry add <package_name>
```

## Install dependencies

```bash
poetry install

#and

pip install -e .
```

## Install all dependencies

```bash
poetry install --with all
```

## Build and publish

```bash
python3 -m pip install --upgrade build
python3 -m build

python3 -m pip install --upgrade twine
python3 -m twine upload --repository testpypi dist/*
```

or

```bash
poetry build
poetry publish
```

## Install a local package

```bash
python3 -m pip install dist/*.whl
```