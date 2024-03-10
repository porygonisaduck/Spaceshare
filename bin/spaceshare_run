#!/bin/bash
# insta485run

# Stop on errors
# See https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
set -Eeuo pipefail

#print commands
set -x

# compile the javascript file
npx webpack

# check if sqlite3 files exists
FILE=./var/spaceshare.sqlite3
if test -f "$FILE"; then
	npx webpack --watch &
	flask --app spaceshare --debug run --host 0.0.0.0 --port 8000 # run app
else
	# echo "Error: can't find database var/spaceshare.sqlite3"
    ./bin/spaceshare_db create
    npx webpack --watch &
    flask --app spaceshare --debug run --host 0.0.0.0 --port 8000
	# echo "Try: ./bin/spaceshare_db create"
	# exit 1
fi
