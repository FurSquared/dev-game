#!/usr/bin/env bash

# Install libaries
cd /var/www/backend
sudo ln -sf /var/www/prod_resources/local_settings.py /var/www/backend/f2game
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --no-input

# Set permission for all files
sudo chown -R www-data:www-data /var/www/

sudo ln -sf /etc/nginx/sites-available/f2game.conf /etc/nginx/sites-enabled

# Restart services
systemctl daemon-reload
sudo systemctl restart gunicorn
sudo systemctl restart nginx
