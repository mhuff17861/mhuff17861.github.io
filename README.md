# Django Portfolio Website App(s)

## Description

Building a portfolio website for myself using Django and Bootstrap. End goal is a django project that will allow a solid portfolio website to be built off of the data the user enters. Going to start of pretty limited, not looking to recreate squarespace or wix hear, but it should be good enough that the user can just enter the necessary data and have a website (with probably a little bit of jank, as a treat)

## Dependencies

- Node Package Manager 8.10^
  - This takes care of other dependencies via the below commands. Check package.json for specifics
- Python 3.10 (Go higher at your own risk, newest at time of original development)
- Postgre Database 14.0^

## Setup

### Development Environment

- Run `npm -i`
- Run `gulp devSetup`
- Setup Python virtual environment for development work
  - Run `python3.10 -m venv portfolioVEnv`
  - Run `source portfolioVEnv/bin/activate`
  - Install Python requirements with `pip install -r requirements.txt`
- Set logging level
  - There is currently only one logger, which looks for the logging level in the environment variable
  DJANGO_LOG_LEVEL. You can set this for your machine, or it will default to WARNING and higher.
- Setup a postgre database (Will automate as much as possible later)
  - The setup_files directory has an sql template for database/user setup.
  - Create a .pg_service.conf file and .pgpass file (templates in setup_files directory) and place them in your home directory. Then run `chmod 0600 .pgpass` to make postgre happy.

### Server Deployment

Coming Soon. I gotta build a website first.

## Known Weirdness

- The password is directly in the settings!?
  - Was going to use pgpass and a pg_service.conf file (see below), but those don't work with testing at the moment, see [this support ticket](https://code.djangoproject.com/ticket/33685). Once I get closer to production there will either be a fix or I'll just make an entry in .gitignore for a secret config file.
- The (currently commented out) Postgre DB settings don't look like the documentation
  - The 'passfile' setting for Postgre did not work. When I got rid of the setting, leaving only the service file link and a chmodded 0600 .pgpass in my home folder (where Postgre expects it), suddenly everything worked.

## Further Documentation

Not available yet. I have comments throughout the files, but haven't decided on a
documentation generator yet.
