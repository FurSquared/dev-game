#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip nginx gunicorn
pip install pipenv
sudo rm -rf /var/www/backend
