#!/bin/bash

#NAME="hello_app"                                  # Name of the application
DJANGODIR=/opt/.virtualenvs/docs-avvocatura/             # Django project directory
APPDIR=/opt/docs-avvocatura/             # Django project directory
SOCKFILE=/opt/docs-avvocatura/gunicorn.sock  # we will communicte using this unix socket
#USER=hello                                        # the user to run as
#GROUP=webapps                                     # the group to run as
NUM_WORKERS=3                                     # how many worker processes should Gunicorn spawn
DJANGO_SETTINGS_MODULE=mongo.settings             # which settings file should Django use
DJANGO_WSGI_MODULE=mongo.wsgi                     # WSGI module name

echo "Starting app as `whoami`"

# Activate the virtual environment
cd $DJANGODIR
source bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
cd $APPDIR
exec $DJANGODIR/bin/gunicorn ${DJANGO_WSGI_MODULE}:application \
  --workers $NUM_WORKERS \
  --bind=unix:$SOCKFILE \
  --log-level=debug \
  --log-file=/tmp/avvocatura.critical

