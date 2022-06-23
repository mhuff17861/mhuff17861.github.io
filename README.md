# Django Portfolio Website App(s)

## Description

**This project is still very much in development.**

The purpose of this project is to build a portfolio website for myself using Django and Bootstrap. The end goal is a django project that will allow a solid portfolio website to be built off of the data the user enters. It's going to start of pretty limited, I'm not looking to recreate Squarespace or Wix here, but it should be good enough that the user can just enter the necessary data and have a website (with a only a little bit of jank, as a treat).

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

Check the docs for server deployment. You can generate them with the following commands:

- `python doc_gen.py`

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

The documentation is under docs/, and is generated via sphinx.
You can generate your own files using the following commands:

- `python doc_gen.py`
