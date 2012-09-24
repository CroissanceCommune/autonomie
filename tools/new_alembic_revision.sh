#!/bin/bash
set -e

echo "Enter revision description:"
read REV_DESC
echo
export CURRENT_VERSION=$(cat ./CURRENT_VERSION)

alembic -c app.ini -n alembic revision -m"$CURRENT_VERSION : $REV_DESC"

echo "You can now edit autonomie/alembic/versions/$(ls -1tr autonomie/alembic/versions/*.py|tail -n1)"
echo "with your mysql migration stuff (alter table add/drop column ...)"
echo

echo "You'll then need to do:"
echo "git add $(ls -1tr autonomie/alembic/versions/*.py|tail -n1)"
echo

echo "Please add other modified files if needed with 'git add ... ', and then:"
echo "  git commit -m '[alembic] $REV_DESC'"
