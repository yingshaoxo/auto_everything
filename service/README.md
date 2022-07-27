# Auto Everything Service
We use frontend technical to show the user interface.

We use Python to make backend API here.

## Env
```bash
poetry shell

brew install llvm

LLVM_CONFIG="/opt/homebrew/Cellar/llvm/14.0.6_1/bin/llvm-config" arch -arm64 python -m pip install llvmlite librosa

poetry install

python -m pip install torchaudio torch torchvision 

python -m pip install tensorflow-macos

python -m pip install speechbrain
```

## Usage
```bash
poetry run dev

cd web
yarn
yarn dev
```

## ~~Docker~~
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
docker build --tag auto_everything_service .

docker run --rm --name the_auto_everything_service auto_everything_service
```