.ONESHELL:
SHELL := /bin/bash

all: build

build:
	python build_dashboard.py

run:
	gunicorn --preload dashboard:app