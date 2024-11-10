cd viamericas
python manage.py makemigrations
python manage.py migrate
python manage.py populate
python manage.py collectstatic --noinput
gunicorn --bind 0.0.0.0:8000 viamericas.wsgi:application --workers=1
