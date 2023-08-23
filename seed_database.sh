#!/bin/bash

rm db.sqlite3
rm -rf ./piratesrareapi/migrations
python manage.py makemigrations piratesrareapi
python manage.py migrate 
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata authors
python manage.py loaddata categories
python manage.py loaddata posts
python manage.py loaddata tags
python manage.py loaddata comments
