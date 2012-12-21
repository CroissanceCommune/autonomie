#!/bin/bash

if [ "$1" == '-f' ]
then
    echo "Forcing"
    MYSQLCMD='mysql -u root'
    DBNAME='egw'
    DBUSER='egw'
    DBPASS='egw'
else
    echo "Enter the mysql command line needed to have root access (default: 'mysql -u root')"
    read MYSQLCMD
    if [ "$MYSQLCMD" == '' ]
    then
        MYSQLCMD='mysql -u root'
    fi
    echo "Enter the database name (default : 'egw')"
    read DBNAME
    if [ "$DBNAME" == '' ]
    then
        DBNAME='egw'
    fi
    echo "Enter the database user (default : 'egw')"
    read DBUSER
    if [ "$DBUSER" == '' ]
    then
        DBUSER='egw'
    fi
    echo "Enter the database user password (default : 'egw')"
    read DBPASS
    if [ "$DBPASS" == '' ]
    then
        DBPASS='egw'
    fi

fi

echo "Deleting database ${DBNAME}"
echo "drop database ${DBNAME};" | ${MYSQLCMD}
echo "create database ${DBNAME};" | ${MYSQLCMD}
echo "grant all privileges on ${DBNAME}.* to ${DBUSER}@localhost identified by '${DBPASS}';" | ${MYSQLCMD}
echo "flush privileges;" | ${MYSQLCMD}
echo "Database reseted"
