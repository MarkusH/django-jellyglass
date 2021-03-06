#!/bin/bash

flake8
isort --recursive --check-only jellyglass tests
coverage run `which django-admin.py` test --pythonpath=./ --settings=tests.settings $@ || exit 1
coverage xml
coverage report -m
