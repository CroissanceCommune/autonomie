#!/bin/bash
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

for table in `echo show tables | $MYSQLCMD $DBNAME | grep -v Tables_in_`; do
        TABLE_TYPE=`echo show create table $table | $MYSQLCMD $DBNAME | sed -e's/.*ENGINE=\([[:alnum:]\]\+\)[[:space:]].*/\1/'|grep -v 'Create Table'`
        if [ $TABLE_TYPE = "MyISAM" ] ; then
                echo "ALTER TABLE $table ENGINE = InnoDB" | $MYSQLCMD $DBNAME
        fi
done
