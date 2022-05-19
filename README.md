# mhuff17861.github.io

## Description

This is the repository I'm using to build my own portfolio website using Django and Bootstrap. Currently only a prototype while I learn Django and do some project planning.

## Dependencies

- Node Package Manager 8.10^
  - This takes care of other dependencies via the below commands. Check package.json for specifics
- Python 3.10 (Go higher at your own risk, newest at time of original development)

## Setup

### Development Environment

- Run `npm -i`
- Run `gulp devSetup`
- Setup Python virtual environment for development work
  - Run `python3.10 -m venv portfolioVEnv`
  - Run `source portfolioVEnv/bin/activate`
  - Install Python requirements with `pip install -r requirements.txt`
- Setup a postgre database
  - The setupscripts directory has an sql template for database/user setup.
  - **Note:** If you want to change the name of the database, make sure to change it in the Django settings as well. You should, at least, change the password for deployments.

### Server Deployment

Coming Soon. I gotta build a website first.

## Know Weirdness

- The Postgre DB settings don't look like the documentation
  - The 'passfile' setting for Postgre did not work. When I got rid of the setting, leaving only the service file link and a chmodded 0600 .pgpass in my home folder (where Postgre expects it), suddenly everything worked. 
