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

#or

poetry add --group all <package_name>
```

## Install auto_everything with all dependencies

```bash
poetry add --extras=all auto_everything

#or

poetry add auto_everything[all]

#or

pip install git+https://github.com/yingshaoxo/auto_everything.git@dev
```

## Add a package and do the developement without reinstall

```bash
poetry add --editable --extras=all .

#and

pip install -e .
```


## Build and publish

```bash
python3 -m pip install --upgrade build
python3 -m build

python3 -m pip install --upgrade twine
python3 -m twine upload dist/*
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