#!/bin/bash
URL=""
FILENAME=""

#COMMAND LINE PARSING
USAGE="Usage: $0 [-h] [-u|--url url] [-l|--listuser]"
CMDPARSER=`getopt -o hu:l: --long help,url:,listuser: -n 'test_connexion.sh' -- "$@"`
if [ $? != 0 ] ; then echo "Terminating..." >&2 ; exit 1 ; fi
eval set -- "$CMDPARSER"
while true ; do
    case "$1" in
        -h|--help)
            echo $USAGE
            exit 0
            ;;
        -u|--url)
            URL=$2
            shift 2
            ;;
        -l|--listuser)
            FILENAME=$2
            shift 2
            ;;
        --) shift ; break ;;
        *)
            echo $USAGE
            exit 1
            ;;
esac
done
if [ "$URL" == "" ]
then
    echo $USAGE
    exit 1
fi
if [ "$FILENAME" == "" ]
then
    echo  $USAGE
    exit 1
fi
echo "* Url to test : $URL"
echo "* User list : $FILENAME"
echo "* logfile : /tmp/testlog.log"
echo "Start tests"
cat $FILENAME | while read LINE
do
    python test_connexion.py $URL $LINE &
done
echo "Done"
