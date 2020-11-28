# Clueless

Track your [Clue](https://en.wikipedia.org/wiki/Cluedo) games with a convenient web app!

Currently it lets you create and track games.

- User authentication coming soon.
- Better input workflow coming soon.
- Optionally catching your obvious mistakes, coming soon.
- "Cheat mode" coming soon... ;)

## How to develop

Assuming you already have Python 3.6 or higher:

```console
$ git clone https://github.com/dabreese00/clue-solver-django.git
$ cd clue-solver-django
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install django
(.venv) $ cd cluesolver
(.venv) $ ./manage.py migrate
(.venv) $ ./manage.py runserver
```

Open a browser, navigate to `127.0.0.1:8000`, and you are up and running!


## How to deploy

Django requires:

- Python 3.6 or higher
- PostgreSQL 9.5 or higher

### The hard way

The hard way is the only way so far.  Stay tuned.

- Ubuntu 18.04
- Install prerequisites:
```console
$ sudo apt -y install \
    python3 python3-venv python3-dev build-essential \
    postgresql supervisor nginx git
```
- Git clone the repository and `cd` into it.
- Create a Python 3 virtualenv.
- Activate the virtualenv and `pip install -r requirements.txt`.
- Setup PostgreSQL database, user and password.
- Setup supervisor to run `gunicorn -b localhost:8000 -w 4 cluesolver.wsgi`.
- Copy Django static files.
- Setup nginx to proxy to gunicorn & serve static files.
- Setup Django settings for production: See [Django Deployment Checklist](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/).


## Life's story

This is a project to help teach myself web development.  It's a successor to my
original [Clue Solver in Flask](https://github.com/dabreese00/clue-solver),
created because I wanted to see how using a different set of tools might allow
me to achieve the same ends with more or less ease and elegance.  By contrast
to the original project (which used handwritten classes stored with pickle),
this Django project naturally does use a traditional database backend.

Currently, the frontend is relatively well-developed (around 70-80% of my
initial goal).

As for the backend, so far it's basically just data storage and some limited
validation.  Plans to add a logical inference engine along the lines of the
original project, but this time as a configurable feature at the user's option.
