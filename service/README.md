# Auto Everything Service
We use frontend technical to show the user interface.

We use Python to make backend API here.

## Env
```bash
conda env update --prefix ./env --file environment.yml  --prune

poetry install

conda install -c conda-forge tensorflow
```

## Usage
```bash
poetry run dev
```