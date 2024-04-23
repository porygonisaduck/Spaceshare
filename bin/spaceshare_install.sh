#!/bin/bash
# spaceshare_install

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

# print commands
set -x

# create python virtual environment
python3 -m venv env

# activate virutal environment
source env/bin/activate

# install back end
pip install -r requirements.txt
pip install -e .

# install front end
npm ci .

