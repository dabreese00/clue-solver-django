# Clueless

Track your [Clue](https://en.wikipedia.org/wiki/Cluedo) games with a convenient web app!

Currently it lets you create and track games.

- User authentication coming soon.
- Better input workflow coming soon.
- Optionally catching your obvious mistakes, coming soon.
- "Cheat mode" coming soon... ;)


## App workflow

The workflow of using the app (assumes you already have the app [up and
running](#how-to-develop), and have [created a
superuser](https://docs.djangoproject.com/en/3.1/intro/tutorial02/#introducing-the-django-admin):

1.  Create a Card Set (currently this can only be done via the Admin
    interface).
2.  Create a new Game, using a chosen Card Set.
3.  Add new Players to the Game (from the Game Dashboard page, which is also
    where you can view the existing players).
4.  Record some Clue Relations (again on the Game Dashboard page, which is also
    where you can view the already-recorded relations).

A Clue Relation is either a Have (we know player X has card Y), a Pass (we know
player X does *not* have card Z), or a Show (we know player X showed one of
card A, card B, or card C to someone, but we may or may not know exactly which
card was shown).  For more details on the theory, see
[here](https://github.com/dabreese00/clue-solver#theory).

As of now, the app will not make any inferences for you.  It just records and
displays back what you input.

Currently there is no way to delete Games, or remove Players from them, except
via the Admin interface.


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

(For Mac, the 3rd line "python3" might be different.  For Windows, the 3rd and
4th lines at least will be different.)


## How to deploy

Django requires:

- Python 3.6 or higher
- PostgreSQL 9.5 or higher

### The hard way

Rough outline (apply sysadmin common sense):

- Ubuntu 18.04
- Install prerequisites:
```console
$ sudo apt -y install python3 python3-venv postgresql supervisor nginx git
```
- Git clone the repository and `cd` into it.
- Create a Python 3 virtualenv.
- Activate the virtualenv and `pip install -r requirements.txt`.
- Setup PostgreSQL database, user and password.
- Setup supervisor to run `gunicorn -b localhost:8000 -w 4 cluesolver.wsgi`.
- Copy Django static files.
- Setup nginx to proxy to gunicorn & serve static files.
- Setup Django settings for production: See [Django Deployment Checklist](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/).

### The new-fangled Docker way

This method has promise because it gives you a production setup that's so
easy and portable, it can almost be your local dev server too.

That said, these instructions by themselves are not enough to produce a proper
production deployment.  I don't honestly know that much yet about running
Docker in production.  See suggestions below, and use at your own risk.

Similarly, this probably goes without saying, but: Just because this is Docker,
doesn't mean I am saying anything about how well this app will scale, if you
decide to try to run it on a cluster for some reason!  I have no idea, and make
no promises about that.


First, install [docker](https://docs.docker.com/get-docker/) and
[docker-compose](https://docs.docker.com/compose/install/).

Then:

```console
git clone https://github.com/dabreese00/clue-solver-django.git
cd clue-solver-django
docker-compose build
docker-compose run webapp python manage.py migrate
docker-compose up
```

The website is served on port 8080.

To stop the containers, press `CTRL+C` in the terminal, or run
`docker-compose down` from another terminal.

You can run `manage.py` commands inside the `webapp` container instance.  While
the containers are stopped, simply type `docker-compose run webapp python
manage.py command_to_run`; for example, `docker-compose run webapp python
manage.py createsuperuser`.

**These are not production settings yet.  You will still need to do some
tweaking.** I don't have all the answers, but here are some suggestions:

- Setup nginx to serve SSL (or put a whole separate HTTP proxy in front of it?).
- Find a better way to distribute the PostgreSQL credentials to the containers.
- Change the container forwarded port(s) if desired.
- As always, review the Django settings and [Django Deployment
  Checklist](https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/).

Finally a security warning: Docker will open ports _even over top of your
firewall rules, for example UFW_.  This seems to be a known Docker issue.  See
[here](https://github.com/chaifeng/ufw-docker) for details and methods to
address, if you are concerned.

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
