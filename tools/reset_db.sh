#!/bin/bash
echo "Resetting db"
if [ "$1" == '-f' ]
then
    echo "Forcing"
    MYSQLCMD='mysql -u root'
    DBNAME='autonomie'
    DBUSER='autonomie'
    DBPASS='autonomie'
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
    echo "Enter the database user (default : 'autonomie')"
    read DBUSER
    if [ "$DBUSER" == '' ]
    then
        DBUSER='autonomie'
    fi
    echo "Enter the database user password (default : 'autonomie')"
    read DBPASS
    if [ "$DBPASS" == '' ]
    then
        DBPASS='autonomie'
    fi

fi

echo "Deleting database ${DBNAME}"
echo "drop database ${DBNAME};" | ${MYSQLCMD}
echo "create database ${DBNAME};" | ${MYSQLCMD}
echo "grant all privileges on ${DBNAME}.* to ${DBUSER}@localhost identified by '${DBPASS}';" | ${MYSQLCMD}
echo "flush privileges;" | ${MYSQLCMD}
echo "Database reseted"
