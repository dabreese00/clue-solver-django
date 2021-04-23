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

Assuming you already have Python 3.8.5 or higher:

```
$ git clone https://github.com/dabreese00/clue-solver-django.git
$ cd clue-solver-django
$ python3 -m venv .venv
$ source .venv/bin/activate
(.venv) $ pip install pip-tools
(.venv) $ pip-sync requirements.txt dev-requirements.txt
(.venv) $ export DJANGO_SECRET_KEY="sosecret"; export DJANGO_ALLOWED_HOSTS="127.0.0.1"; export DJANGO_DEBUG=True; export DATABASE_URL="sqlite:///db.sqlite3"
(.venv) $ ./manage.py migrate
(.venv) $ ./manage.py collectstatic
(.venv) $ ./manage.py test
(.venv) $ ./manage.py runserver
```

(The 3rd line "python3" might be different depending on your OS; you should use your system's Python 3 binary, whatever it's called.)


## How to deploy

System requirements:

- Python 3.8.5 or higher
- PostgreSQL 9.5 or higher


### The hard way

Rough outline (apply sysadmin common sense):

- Ubuntu 20.04
- Install prerequisites:
```
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

Don't forget SSL (best use Let's Encrypt).

Then you can use PostgreSQL dumps and/or Django dumps for backup and recovery.

Consider using the "easy" way, below, instead -- it takes advantage of a cool
application pattern that allows for much faster and more automated deployment
and maintenance.


### The "easy" way

I've made this repo conform to the [12-factor app](https://12factor.net/)
pattern, so it can be easily deployed on services like Heroku and Dokku.  These
services enable nearly-automated deployment and maintenance processes, by
cleanly decoupling the application code from its supporting services (e.g.
databases) and configuration, and precisely specifying how and where these
separate components come together.

Heroku has plenty of good docs, if you want to spend the money there.

Otherwise, below are the steps to Dokku it up.  This is definitely not a
comprehensive production deployment yet, it still needs some security review;
but it gets the app up and running, with SSL and backups, in potentially less
than 30 minutes if you have a Dokku server already (or if you use e.g. the
DigitalOcean pre-built Dokku template).

- Set up a [Dokku](http://dokku.viewdocs.io/dokku/) server.
- Optional: If you want Let's Encrypt certificate later on, give your Dokku
  server a public IP and DNS A record now.
- On the Dokku server, run the following command as root/with sudo:

```
sudo dokku plugin:install https://github.com/dokku/dokku-postgres.git
```

- Either on the Dokku server, or remotely via SSH, run the following commands
  to pre-configure the app and the database:

```
dokku apps:create clue-solver-django
dokku postgres:create cluesolverdb
dokku postgres:link cluesolverdb clue-solver-django
```

- Then run these additional commands to set the environment variables to
  configure Django:

```
dokku config:set clue-solver-django DJANGO_SECRET_KEY="$(openssl rand -base64 64)"  # this may fail at first, if so either try a few times, or just run the openssl command separately instead of in a subshell
dokku config:set clue-solver-django DJANGO_ALLOWED_HOSTS="cluesolver.dokku.fqdn.me,dokku.fqdn.me"
```

- Finally, git push to the Dokku server, to deploy the app:

```
git remote add dokku dokku@dokku.fqdn.me:clue-solver-django
git push dokku master
```

After this, the web app should be available; either via a subdomain or via a
port number, depending on how you configured Dokku during installation.  If
you're doing it the ports way, make sure to check your firewall, and if needed
you can use "dokku proxy:ports" commands to change port mappings.  If you're
doing it the subdomain way, you'll need to make sure you have a DNS record
pointing the subdomain to the public IP address of your Dokku server.

Database migrations were already performed automatically during the `git push`
(thanks to the "release" line in the Procfile).

Finally, get an SSL cert with [Let's Encrypt via
Dokku](https://github.com/dokku/dokku-letsencrypt):

```
sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
dokku domains:add clue-solver-django dokku.fqdn.me
config:set --no-restart clue-solver-django DOKKU_LETSENCRYPT_EMAIL=your@email.tld
dokku letsencrypt clue-solver-django
```

Optionally you can add a cron job to auto-renew all certificates when needed:
`dokku letsencrypt:cron-job --add`.


#### Backup and recovery

App data:

```
# Backup
dokku postgres:export cluesolverdb > cluesolverdb.dump
# Recover
dokku postgres:import cluesolverdb < cluesolverdb.dump
```

Set up a job to regularly create and offsite these DB dumps.


#### Other Maintenance

Running Django management commands example:

```
dokku run clue-solver-django python manage.py createsuperuser
```

Ensure that if you're using SSH, you use the `-t` option or `RequestTTY` in
your config file, so that you can get an interactive terminal.

You shouldn't ever have to run `collectstatic` or `migrate` this way, because
the Dokku/Procfile machinery is taking care of that automatically during each
re-deployment.


### Notes from behind the scenes of the "easy" way

This Dokku deployment method is easy to do now, but it was *not* easy to get
working in the first place.  Heroku has great, detailed docs for deploying
specific types of apps, but Dokku does not.  And Heroku's deployment for Django
is different enough from Dokku's, that it becomes quite difficult to sort out

The main difficulty I had was understanding *how your Django project should be
set up, to properly interact with Dokku*.

Neither Django's nor Dokku's official documentation currently covers this
almost at all.  And all the unofficial how-to's and blogs I found were
outdated, incomplete, assumed a project file structure very different than the
default Django tree I'm familiar with -- without explaining which
customizations were actually necessary for Dokku -- and/or used a Dockerfile
instead of a native Buildpack for some reason.

I'm noting here some of the insights and resources that I found useful in
learning how this works, in case I need to review one day.

Key components in your Django repository/config:

- Use [WhiteNoise](http://whitenoise.evans.io/en/stable/django.html) to serve
  static files.  This avoids the need for a separate service/proxy.
- Add a `Procfile` that specifies the command to run your WSGI app.  See Heroku
  docs/examples or borrow from [this
  cookiecutter](https://github.com/pydanny/cookiecutter-django).
- Add a `runtime.txt` file that specifies your Python version.  See [Heroku
  examples](https://github.com/heroku/python-getting-started).
- You will probably need to edit your Django settings (see below).
- Make sure you have a `requirements.txt` file in your repository root.  This
  helps Heroku/Dokku detect that you have a Python app.
- You may need to make sure your git repository's root is also the root of your
  Django project (i.e. the folder where `manage.py` lives).  I've not seen
  anyone explicitly say this is a 12-factor (or Heroku or Dokku) requirement,
  but I also couldn't find any examples of people doing otherwise.  At the very
  least, to do differently seems to require some less-than-elegant
  work-arounds. I couldn't get it to work, and eventually gave up and just
  re-structured my git repo to fit this format.

Notes on Django settings and environment variables (the hardest part, for me at
least):

- Alter your Django `settings.py` file to read variables from the environment.
  Any variables that differ between dev and production should be read this way,
  instead of being "hard-coded" into the settings file -- in particular,
  `DEBUG`, `SECRET_KEY`, `ALLOWED_HOSTS`, and `DATABASES`, maybe others too.
- Heroku and Dokku will feed your app an environment variable called
  `DATABASE_URL`, which needs to be parsed during your Django configuration to
  create your Django `DATABASES['default']` dictionary.
- [This package](https://django-environ.readthedocs.io/en/latest/) can help
  with reading the Django configuration from the environment, including parsing
  the `DATABASE_URL`.
- Set your dev configuration variables using a `.env` file (which you can add
  to your `.gitignore`).
- Set your production configuration variables using `dokku config:set` (aside
  from `DATABASE_URL`, which Heroku/Dokku will set automatically).
- If you want to convert your default local SQLite database config into a
  Heroku/Dokku-style `DATABASE_URL`, something like `sqlite:///db.sqlite3`
  represents a relative file path of `db.sqlite3` (presumably, relative to the
  directory from which `manage.py` is executed?) -- this seems to have the
  results I wanted so far.

Other resources I found helpful:

- Create a free Heroku account and do the Python getting started tutorial.  It
  doesn't directly translate to Dokku, but it helps give a feel for it.
- Helpful boilerplate template, as a working example to emulate (although way
  overkill for my needs): https://github.com/pydanny/cookiecutter-django
- From the same boilerplate, instructions for Heroku (again doesn't translate
  to Dokku 100%, but gives some useful pointers):
  https://cookiecutter-django.readthedocs.io/en/latest/deployment-on-heroku.html


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
