#!/usr/bin/env bash

# call out local_settings
export DJANGO_SETTINGS_MODULE=f2game.local_settings

# Install libaries
cd /var/www/backend
sudo ln -sf /var/www/prod_resources/local_settings.py /var/www/backend/f2game
pipenv install
pipenv run python manage.py migrate
pipenv run python manage.py collectstatic --no-input

# Set permission for all files
sudo chown -R www-data:www-data /var/www/

sudo ln -sf /etc/nginx/sites-available/f2game.conf /etc/nginx/sites-enabled

# Restart services
systemctl daemon-reload

sudo systemctl enable gunicorn
sudo systemctl enable nginx

sudo systemctl restart gunicorn
sudo systemctl restart nginx
