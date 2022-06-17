# Django Portfolio Website App(s)

## Description

**This project is still very much in development.**

Building a portfolio website for myself using Django and Bootstrap. End goal is a django project that will allow a solid portfolio website to be built off of the data the user enters. Going to start of pretty limited, I'm not looking to recreate Squarespace or Wix here, but it should be good enough that the user can just enter the necessary data and have a website (with a only a little bit of jank, as a treat).

## Dependencies

- Node Package Manager 8.12^
- Python 3.10 (Go higher at your own risk, newest at time of original development)
- Postgre Database 14.0^

## Setup (aiming to automate later, check full-automation branch)

### Development Environment

- Make sure you have the above dependencies met.
  - Here's what you can get via apt: `sudo apt install python3.10 python3.10-dev python3.10-pip libpq-dev postgresql postgresql-contrib nginx curl`
  - I recommend [fnm](https://github.com/Schniz/fnm#using-a-script-macoslinux) for your node/npm install
- Run `npm install`
- Run `gulp devSetup`
  - **NOTE:** If gulp does not run, you may need to install it globally. Run `npm install -g gulp-cli`
- Setup Python virtual environment for development work
  - Run `python3.10 -m venv portfolioVEnv`
  - Run `source [yourVenvName]/bin/activate`
  - Install Python requirements with `pip install -r requirements.txt`
- Set environment variable DJANGO_SETTINGS_MODULE to portfoliosite.dev_settings
  - `export DJANGO_SETTINGS_MODULE=portfoliosite.dev_settings`
- Set logging level
  - There is currently only one logger, which looks for the logging level in the environment variable
  DJANGO_LOG_LEVEL. You can set this for your machine, or it will default to WARNING and higher.
  - `export DJANGO_LOG_LEVEL=DEBUG`
- Setup a postgre database
  - Login to postgre as superuser, `sudo -u postgres psql`
  - The setup_files directory has an sql template for database/user setup. Run each command in psql
    - You cam sub in your own names if you want, but you'll have to change the appropriate settings in dev_settings.py
  - `\q` to quit psql
  - **NOTE: The following setup step does not work yet due to a django bug. See known weirdness section below**  Create a .pg_service.conf file and .pgpass file (templates in setup_files directory) and place them in your home directory. Then run `chmod 0600 .pgpass` to make postgre happy.
- Go into the Django project folder (portfoliosite), and run the following two commands
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - `python manage.py createsuperuser`
- Test the setup with the following commands
  - `python manage.py test`
  - `python manage.py runserver`

### Server Deployment

- Make sure you have the above dependencies met.
  - Here's what you can get via apt: `sudo apt install python3.10 python3.10-dev python3.10-pip libpq-dev postgresql postgresql-contrib nginx curl`
  - I recommend [fnm](https://github.com/Schniz/fnm#using-a-script-macoslinux) for your node/npm install
- Run `npm install`
- Run `gulp prodSetup`
  - **NOTE:** If gulp does not run, you may need to install it globally. Run `npm install -g gulp-cli`
  - **NOTE: You will want to change the sassDest and jsDest variables in gulpfile.js. Change your production_settings.py STATIC variables to align with that folder choice**
- Setup Python virtual environment for development work
  - Run `python3.10 -m venv portfolioVEnv`
  - Run `source [yourVenvName]/bin/activate`
  - Install Python requirements with `pip install -r requirements.txt`
- Set environment variable DJANGO_SETTINGS_MODULE to portfoliosite.dev_settings
  - `export DJANGO_SETTINGS_MODULE=portfoliosite.production_settings`
- Set logging level
  - There is currently only one logger, which looks for the logging level in the environment variable
  DJANGO_LOG_LEVEL. You can set this for your machine, or it will default to WARNING and higher.
  - `export DJANGO_LOG_LEVEL=DEBUG`
- Create credentials.json
  - Under setup_files/data_templates/, there is a template credentials.json. Fill in the information
  and then place it in /etc/
  - You can generate a Django secret key with by going into the Django shell
    - `python manage.py shell`
    -  `from django.core.management.utils import get_random_secret_key`
    -  `get_random_secret_key()`
- Setup a postgre database
  - Login to postgre as superuser, `sudo -u postgres psql`
  - The setup_files directory has an sql template for database/user setup. Run each command in psql, using the settings you put in your credentials.json file
    - You can subtitute in your own names if you want, but you'll have to change the appropriate settings in dev_settings.py
  - `\q` to quit psql
  - **NOTE: The following setup step does not work yet due to a django bug. See known weirdness section below**  Create a .pg_service.conf file and .pgpass file (templates in setup_files directory) and place them in your home directory. Then run `chmod 0600 .pgpass` to make postgre happy.
- Go into the Django project folder (portfoliosite), and run the following two commands
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - `python manage.py createsuperuser`
  - `python manage.py collectstatic`
- Add your own domains/ip addresses to ALLOWED_HOSTS in production_settings.py
- Move gunicorn.socket and gunicorn.service (in the setup_files/web_server folder) to `/etc/systemd/system/`\
  - Edit `/etc/systemd/system/gunicorn.service` so that the User, Working Directory, and ExecStart are pointing to the correct place.
- Add your user to the www-data group
  - `sudo groupadd www-data`
  - `sudo usermod -a -G www-data [yourserveruserhere]`
- Start the gunicorn service
  - `sudo systemctl start gunicorn.socket`
  - `sudo systemctl enable gunicorn.socket`
  - Check with `sudo systemctl status gunicorn.socket`
- Setup Nginx to serve static files
  - There are setup files in `setup_files/web_server`
  - You'll need to change the paths in the file to fit your server
  - Move the file to `/etc/nginx/sites-available/[site-name]`
  - Run the command `sudo ln -s /etc/nginx/sites-available/[site-name] /etc/nginx/sites-enabled`
  - Check the syntax with `sudo nginx -t`
  - Start service with `sudo systemctl restart nginx`
  - Give necessary permissions with `sudo ufw allow 'Nginx Full'`
- Test by connecting to your servers ip address (or url if you have that setup with your nameserver)

## Branch Layout

- main
  - testing
    - development
      - feature implementation branches

## Known Weirdness

- You're using postgre, but not pgpass?
  - I was going to use pgpass and a pg_service.conf file (see below), but those don't work with testing at the moment, see [this support ticket](https://code.djangoproject.com/ticket/33685). So for now I have a template credentials file that just gets imported. This is a personal website I'm just trying
  to get out of the door, so while I have some security concerns, I'll worry about locking down everything more thoroughly later.
- The (currently commented out) Postgre DB settings don't look like the documentation
  - The 'passfile' setting for Postgre did not work. When I got rid of the setting, leaving only the service file link and a chmodded 0600 .pgpass in my home folder (where Postgre expects it), suddenly everything worked.

## Further Documentation

### Django Docs

#### Python files

The documentation is under docs/, generated via sphinx. Currently it only covers django python and template files. You can generate your own if you make edits to the docstrings in the files using the following commands

- `python doc_gen.py`
- `CI_MAKING_DOCS=1 sphinx-build docs/source docs/build/html`
