#!/bin/sh

python manage.py migrate
python manage.py loaddata database_models_fixture.json
python manage.py crontab add
python manage.py runserver 0.0.0.0:8000