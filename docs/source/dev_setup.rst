Development Environment Setup
=============================

-  Make sure you have the above dependencies met.

   -  Here's what you can get via apt:
      ``sudo apt install python3.10 python3.10-dev python3.10-pip libpq-dev postgresql postgresql-contrib nginx curl``
   -  I recommend
      `fnm <https://github.com/Schniz/fnm#using-a-script-macoslinux>`__
      for your node/npm install

-  Run ``npm install``
-  Run ``gulp devSetup``

   -  **NOTE:** If gulp does not run, you may need to install it
      globally. Run ``npm install -g gulp-cli``

-  Setup Python virtual environment for development work

   -  Run ``python3.10 -m venv portfolioVEnv``
   -  Run ``source [yourVenvName]/bin/activate``
   -  Install Python requirements with
      ``pip install -r requirements.txt``

-  Set environment variable DJANGO_SETTINGS_MODULE to
   portfoliosite.dev_settings

   -  ``export DJANGO_SETTINGS_MODULE=portfoliosite.dev_settings``

-  Set logging level

   -  There is currently only one logger, which looks for the logging
      level in the environment variable DJANGO_LOG_LEVEL. You can set
      this for your machine, or it will default to WARNING and higher.
   -  ``export DJANGO_LOG_LEVEL=DEBUG``

-  Setup a postgre database

   -  Login to postgre as superuser, ``sudo -u postgres psql``
   -  The setup_files directory has an sql template for database/user
      setup. Run each command in psql

      -  You cam sub in your own names if you want, but you'll have to
         change the appropriate settings in dev_settings.py

   -  ``\q`` to quit psql
   -  **NOTE: The following setup step does not work yet due to a django
      bug. See known weirdness section below** Create a .pg_service.conf
      file and .pgpass file (templates in setup_files directory) and
      place them in your home directory. Then run ``chmod 0600 .pgpass``
      to make postgre happy.

-  Go into the Django project folder (portfoliosite), and run the
   following two commands

   -  ``python manage.py makemigrations``
   -  ``python manage.py migrate``
   -  ``python manage.py createsuperuser``

-  Test the setup with the following commands

   -  ``python manage.py test``
   -  ``python manage.py runserver``
