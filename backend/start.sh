#!/bin/bash

pip install --upgrade pip
pip install -r /app/requirements.txt

gunicorn infracloud:api -b 0.0.0.0:1234
