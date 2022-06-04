# Django Portfolio Website App(s)

## Description

Building a portfolio website for myself using Django and Bootstrap. End goal is a django project that will allow a solid portfolio website to be built off of the data the user enters. Going to start of pretty limited, I'm not looking to recreate Squarespace or Wix here, but it should be good enough that the user can just enter the necessary data and have a website (with a only a little bit of jank, as a treat).

## Dependencies

- Node Package Manager 8.12^
  - This takes care of other dependencies via the below commands. Check package.json for specifics
- Python 3.10 (Go higher at your own risk, newest at time of original development)
- Postgre Database 14.0^

## Setup

### Development Environment (aiming to automate later, check full-automation branch)

- Run `npm install`
- Run `gulp devSetup`
- Setup Python virtual environment for development work
  - Run `python3.10 -m venv portfolioVEnv`
  - Run `source portfolioVEnv/bin/activate`
  - Install Python requirements with `pip install -r requirements.txt`
- Set environment variable DJANGO_SETTINGS_MODULE to portfoliosite.dev_settings
  - `export DJANGO_SETTINGS_MODULE=portfoliosite.dev_settings`
  - May want to put in your respective .rc file to maintain between shell sessions
- Set logging level
  - There is currently only one logger, which looks for the logging level in the environment variable
  DJANGO_LOG_LEVEL. You can set this for your machine, or it will default to DEBUG and higher.
  - `export DJANGO_LOG_LEVEL=DEBUG`
- Setup a postgre database
  - The setup_files directory has an sql template for database/user setup.
  - **NOTE: The following setup step does not work yet due to a django bug. See known weirdness section below**  Create a .pg_service.conf file
  and .pgpass file (templates in setup_files directory) and place them in your home directory. Then run `chmod 0600 .pgpass` to make postgre happy.

### Server Deployment

Coming Soon. I gotta build a website first. All instructions below are just for my own tracking purposes/notes for
future automation.

- Create credentials.json
  - Under setup_files/data_templates/, there is a template credentials.json. Fill in the information
  and then place it in /etc/
- Set environment variable DJANGO_SETTINGS_MODULE to portfoliosite.dev_settings
  - `export DJANGO_SETTINGS_MODULE=portfoliosite.production_settings`
- Set logging level
  - There is currently only one logger, which looks for the logging level in the environment variable
  DJANGO_LOG_LEVEL. You can set this for your machine, or it will default to WARNING and higher.
  - `export DJANGO_LOG_LEVEL=WARNING`

## Known Weirdness

- You're using postgre, but not pgpass?
  - I was going to use pgpass and a pg_service.conf file (see below), but those don't work with testing at the moment, see [this support ticket](https://code.djangoproject.com/ticket/33685). So for now I have a template credentials file that just gets imported. This is a personal website I'm just trying
  to get out of the door, so while I have some security concerns, I'll worry about locking down everything more thoroughly later.
- The (currently commented out) Postgre DB settings don't look like the documentation
  - The 'passfile' setting for Postgre did not work. When I got rid of the setting, leaving only the service file link and a chmodded 0600 .pgpass in my home folder (where Postgre expects it), suddenly everything worked.

## Further Documentation

Not available yet. I have comments throughout the files, but haven't decided on a
documentation generator yet (especially since, to my knowledge, I can't autogenerate
Django template docs).
