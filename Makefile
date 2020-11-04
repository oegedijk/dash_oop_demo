.ONESHELL:
SHELL := /bin/bash

all: 

run:
	gunicorn --preload dashboard:app