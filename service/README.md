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

## Docker
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
docker build --tag auto_everything_service .

docker run --rm --name the_auto_everything_service auto_everything_service
```