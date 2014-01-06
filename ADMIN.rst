Autonomie Administration
========================

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

Alembic is used every time we changed the database schema.

Add a new revision::

    tools/new_alembic_revision.sh

Then, migrate::

    autonomie-migrate app.ini upgrade

Debian dependencies
-------------------

Install::
    apt-get install python-dev libmysqlclient-dev build-essential
