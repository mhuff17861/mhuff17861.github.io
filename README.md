# mhuff17861.github.io

## Description

This is the repository I'm using to build my own portfolio website using Django and Bootstrap. Currently only a prototype while I learn Django and do some project planning.

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
