#!/usr/bin/sh
PYTHON_VERSION=$(python3 -V | sed -r 's/.*?(3\.[0-9]).*/\1/')
patch "$@" $VIRTUAL_ENV/lib/python$PYTHON_VERSION/site-packages/untdl/__init__.py < untdl.patch
patch "$@" $VIRTUAL_ENV/lib/python$PYTHON_VERSION/site-packages/untdl/__tcod.py < untdl_noise.patch
