#!/bin/bash
ORIG_DIR=/root/autonomie
WWW_DIR=/var/www/autonomie
LOG_DIR=/var/log/autonomie
CACHE_DIR=/var/cache/autonomie
FILE_DIR=/var/intranet_files/files
TMP_DIR=/tmp/garbage/

if [ "$1" == '' ]
then
    echo "Missing the url of your website that should be passed as first argument"
    exit 1
fi

if [ ! -d ${ORIG_DIR} ]
then
    echo "Missing ${ORIG_DIR}, Exiting \n"
    exit 1
fi

if [ ! -d ${WWW_DIR} ]
then
    echo "Creating virtualenv ... \n"
    virtualenv -- no-site-packages ${WWW_DIR}
    echo " - > Done\n"
fi

echo "Specific package installation"
apt-get install apache2 libapache2-mod-wsgi python-mysqldb libmysqlclient-dev python2.6-dev mariadb-server-5.5

echo "Installing autonomie\n"
source ${WWW_DIR}/bin/activate

# Removing existing datas
rm -rf ${WWW_DIR}/autonomie/

# Copying source files
cp -R ${ORIG_DIR} ${WWW_DIR}/autonomie
cd ${WWW_DIR}/autonomie
rm -rf ${WWW_DIR}/autonomie/.git*
python setup.py develop

echo " + Setting up conf files + "
python ${ORIG_DIR}/deploy_scripts/all.py $1 $2 $3
hostname $1

rsync -av ${TMP_DIR} /
rm -rf ${TMP_DIR}

# Cache directories
/bin/mkdir -p ${CACHE_DIR}/beaker
/bin/mkdir -p ${CACHE_DIR}/mako
/bin/rm -rf ${CACHE_DIR}/mako/*
/bin/rm -rf ${CACHE_DIR}/beaker/*

#Log directories
/bin/mkdir -p ${LOG_DIR}
chown -R www-data ${LOG_DIR}
chmod -R o-rwx ${LOG_DIR}

# Datas storing
/bin/mkdir -p ${FILE_DIR}/main
chown -R www-data ${FILE_DIR}
chmod -R o-rw ${FILE_DIR}

#logrotate
echo """
${LOG_DIR}/*.log {
    weekly
    missingok
    rotate 4
    compress
    delaycompress
    notifempty
    create 640 www-data
    sharedscripts
    postrotate
        /etc/init.d/apache2 reload > /dev/null
    endscript
}""" > /etc/logrotate.d/autonomie


echo " - > Done\n"
echo "Setting rights\n"
chown -R www-data:www-data ${CACHE_DIR}
chmod -R o-rwx ${CACHE_DIR}

chown -R www-data:www-data *
chmod -R o-rwx *
echo " - > Done\n"

echo "Installation is done"
service apache2 restart
exit 0
