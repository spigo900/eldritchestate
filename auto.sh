#!/bin/sh
ls src/py/*.py | entr -r python src/py/main.py
