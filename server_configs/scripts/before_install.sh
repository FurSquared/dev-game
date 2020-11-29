#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip nginx gunicorn virtualenv
sudo rm -rf /var/www/backend
