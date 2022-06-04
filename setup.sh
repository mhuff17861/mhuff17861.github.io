#!/usr/bin/env bash

# set_environment_variables () {
#   echo "Setting environment variables"
#   export DJANGO_LOG_LEVEL="WARNING"

#   Following should be an if depending on production or development
#   export DJANGO_SETTINGS_MODULE=portfoliosite.dev_settings OR
#   export DJANGO_SETTINGS_MODULE=portfoliosite.production_settings
# }

setup_python () {
  echo "Setting up python 3.10"

  #Initial install
  add-apt-repository --y ppa:deadsnakes/ppa
  apt-get -qq update && apt-get -qq --assume-yes install python3.10 python3.10-dev python3.10-venv libpq-dev

  # Setup Venv
  # python3.10 -m venv portfolioVEnv
  # source portfolioVEnv/bin/activate
  # pip install -r requirements.txt
}

setup_node () {
  echo "Setting up node"
  ###APT REPO BAD. Need to do snap or something else.
  ## FNM seems nice, no idea how to get npm though
  apt-get -qq update && apt-get -qq --assume-yes install nodejs npm
  # npm install
  # Likely need to install gulp-cli globally.... hmmm......
}

setup_static_files () {
  echo "Setting up static files using gulp"
  gulp devSetup
}

setup_postgre_database () {
  echo "Setting up Postgre"
  apt-get -qq update && apt-get -qq --assume-yes install postgresql postgresql-contrib

  psql -f setup_files/postgre-setup-template.sql
}

setup_django_admin () {
  echo "Setting up django"

  # source portfolioVEnv/bin/activate
  # python portfoliosite/manage.py createsuperuser
  # python portfoliosite/manage.py makemigrations
  # python portfoliosite/manage.py migrate
  # Gotta do a collect static for

  #HEEEEEYYYYYYYY The asgi.py was defaulting to the wrong settings file for gunicorn. Double
  # check on install!!!!
}

setup_web_server () {
  echo "Setting up web server"
}

# Check for sudo
if [ $(id -un) != "root" ]; then
  echo "This script requires root permissions"
  sudo "$0" "$@"
  exit
fi

# Run everthing
setup_python
setup_node
setup_static_files
setup_postgre_database
setup_django_admin
setup_web_server
