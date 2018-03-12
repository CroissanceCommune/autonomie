#!/bin/bash
echo "Setting 'o' password for everyone"
if [ "$1" == '-f' ]
then
    echo "Forcing"
    MYSQLCMD='mysql -u root'
    DBNAME='autonomie'
else
    echo "Enter the mysql command line needed to have root access (default: 'mysql -u root')"
    read MYSQLCMD
    if [ "$MYSQLCMD" == '' ]
    then
        MYSQLCMD='mysql -u root'
    fi
    echo "Enter the database name (default : 'autonomie')"
    read DBNAME
    if [ "$DBNAME" == '' ]
    then
        DBNAME='autonomie'
    fi
fi

echo "update login set pwd_hash=MD5('o');" | ${MYSQLCMD} ${DBNAME}
