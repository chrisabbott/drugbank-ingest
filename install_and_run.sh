#!/bin/bash

# Set up virtualenv
VIRTUALENV="$1"
PY_VERSION="3.9.0"

if [ ! -r ~/.pyenv/ ]
then
    git clone https://github.com/pyenv/pyenv.git ~/.pyenv
    git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv
fi

export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv install --skip-existing "$PY_VERSION"
pyenv virtualenv "$PY_VERSION" "$VIRTUALENV" &> /dev/null
pyenv activate "$VIRTUALENV" &> /dev/null

# Dependencies
pip install -r requirements.txt --quiet --disable-pip-version-check

# Run
python ingest.py --verbosity=DEBUG scrape-all

# Clean up virtualenv
# pyenv virtualenv-delete --force "$VIRTUALENV"
