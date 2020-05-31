#!/bin/bash
cd web

pipenv run gunicorn -c ../gunicorn_config.py config.wsgi
