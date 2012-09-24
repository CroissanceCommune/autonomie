Autonomie README
================

Getting Started
---------------

The fr_FR.UTF8 locale must be installed::

    dpkg-reconfigure locales

Create the mysql tables::

    create database egw;
    grant all privileges on egw.* to egw@localhost identified by "egw";
    flush privileges;

Install autonomie::

    mkvirtualenv autonomie
    python setup.py develop

Configure autonomie::
    cp development.ini.sample app.ini
    edit app.ini

Serve autonomie::
    pserve app.ini


Alembic migration
-----------------

Add a new revision::

    export REV_DESC="My revision description"
    export CURRENT_VERSION=$(cat ./CURRENT_VERSION)
    alembic -c app.ini -n alembic revision -m"$CURRENT_VERSION $REV_DESC"
    cd autonomie/alembic/versions
    export LAST_FILE=$(ls -1tr|tail -n1)
    mv $LAST_FILE ${CURRENT_VERSION}_${LAST_FILE}
    git add ${CURRENT_VERSION}_${LAST_FILE}

Add the other modified files::

    git add ...
    git commit -m "[alembic] $REV_DESC"

Then, migrate::

    autonomie-migrate app.ini upgrade

Debian dependencies
-------------------

Install::
    apt-get install python-dev libmysqlclient-dev build-essential
