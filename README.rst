Autonomie README
================

Getting Started
---------------

:

    mkvirtualenv autonomie
    python setup.py develop
    cp development.ini.sample app.ini
    # Edit the file
    pserve app.ini


Alembic migration
-----------------

migrate:

    migrate app.ini upgrade

add a new revision:

    alembic -c app.ini -n alembic revision -m"my_revision_name"
