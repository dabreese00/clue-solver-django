release: python manage.py migrate

web: gunicorn cluesolver.wsgi --pythonpath '/app/cluesolver' --log-file -
