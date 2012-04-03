#!/bin/bash
# Initialize a sample mysql database
. Tools

USAGE="Usage: $0 [-h] [-u|--user mysqluser] [-p|--password mysqlpassword] [--nopassword]\n
\tuser             The mysql user with database write and user create access
\tmysqlpassword    The user's password
\tnopassword  If you want to connect to mysql without password \n"


CMDPARSER=`getopt -o hu:p: --long help,user,password,nopassword -n 'init_db.sh' -- "$@"`
log "Command-line parsing"
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$CMDPARSER"
while true ; do
    case "$1" in
        -h|--help)
            echo -e $USAGE
            exit 0
            ;;
        -u|--user)
            BDD_ROOT_USER=$2
            shift 2
            ;;
        -p|--password)
            BDD_ROOT_PWD=$2
            shift 2
            ;;
        --nopassword)
            NOPASSWORD=1
            shift 1
            ;;
        --) shift ; break ;;
        *)
            echo -e $USAGE
            exit 1
            ;;
    esac
done

DBUSER="test"
DBNAME="test"
DBPASS="test"
FILENAME="./sample_db/db.sql"
DATAFILE="./sample_db/testdatas.sql"

if [ "$BDD_ROOT_USER" == "" ]
then
    BDD_ROOT_USER="root"
    log "Using default mysql login : root"
fi
if [ "$BDD_ROOT_PWD" == "" ]
then
    NOPASSWORD=1
fi

if [ ! -f $FILENAME ]
then
    log "ERROR : SQL sample file could not be found. Please launch the script from its current folder."
    exit 1
fi

log "Creating User and database"
my_add ${DBNAME} ${DBUSER} ${DBPASS}
log "Dumping schemas"
mysql_set_db ${DBNAME} ${FILENAME}
log "Dumping datas"
mysql_filedump ${DBNAME} ${DATAFILE}
log "Done"

