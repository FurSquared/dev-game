#!/usr/bin/env bash

# call out local_settings
export DJANGO_SETTINGS_MODULE=f2game.local_settings

# Install libaries
cd /var/www/backend
sudo ln -sf /var/www/prod_resources/local_settings.py /var/www/backend/f2game
sudo -u www-data pipenv install
sudo -u www-data pipenv shell
python manage.py migrate
python manage.py collectstatic --no-input

# Set permission for all files
sudo chown -R www-data:www-data /var/www/

sudo ln -sf /etc/nginx/sites-available/f2game.conf /etc/nginx/sites-enabled

# Restart services
systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
