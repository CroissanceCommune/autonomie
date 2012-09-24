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

Migrate::

    autonomie-migrate app.ini upgrade

Add a new revision::

    alembic -c app.ini -n alembic revision -m"my revision description"


Debian dependencies
-------------------

Install::
    apt-get install python-dev libmysqlclient-dev build-essential
