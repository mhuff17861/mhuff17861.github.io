#!/usr/bin/env bash

# set_environment_variables () {
#   echo "Setting environment variables"
#   export DJANGO_LOG_LEVEL="WARNING"
# }

setup_python () {
  echo "Setting up python 3.10"

  #Initial install
  add-apt-repository --y ppa:deadsnakes/ppa
  apt-get -qq update && apt-get -qq --assume-yes install python3.10 python3.10-dev libpq-dev

  # Setup Venv
  # python3.10 -m venv portfolioVEnv
  # source portfolioVEnv/bin/activate
  # pip install -r requirements.txt
}

setup_node () {
  echo "Setting up node"
  apt-get -qq update && apt-get -qq --assume-yes install nodejs npm
  # npm -i
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
