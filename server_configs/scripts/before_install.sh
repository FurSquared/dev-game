#!/usr/bin/env bash

sudo apt-get update
sudo apt-get install -y python3 python3-pip nginx gunicorn awscli

sudo snap install core
sudo snap refresh core
sudo snap install --classic certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot

pip3 install pipenv
sudo rm -rf /var/www/backend
