#!/bin/bash
echo $HOST
python manage.py migrate
#python data_migration.py
python manage.py runserver 0.0.0.0:8045 --noreload
