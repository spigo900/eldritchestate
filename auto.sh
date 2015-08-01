#!/bin/sh
while sleep 1; do
    ls src/py/eldestrl/**.py | entr -r python src/py/eldestrl/main.py
done
