#!/bin/bash
ORIG_DIR=/root/autonomie
WWW_DIR=/var/www/autonomie
LOG_DIR=/var/log/autonomie
CACHE_DIR=/var/cache/autonomie

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

echo "Installing autonomie\n"
source ${WWW_DIR}/bin/activate

# Removing existing datas
rm -rf ${WWW_DIR}/autonomie/

# Copying source files
mv ${ORIG_DIR} ${WWW_DIR}/autonomie
cd ${WWW_DIR}/autonomie
rm -rf .git*
python setup.py develop

# Cache directories
/bin/mkdir -p ${CACHE_DIR}/beaker
/bin/mkdir -p ${CACHE_DIR}/mako
/bin/rm -rf ${CACHE_DIR}/mako/*
/bin/rm -rf ${CACHE_DIR}/beaker/*

#Log directories
/bin/mkdir -p ${LOG_DIR}
chown -R www-data ${LOG_DIR}

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
}""" > /etc/logrotate.d/autonomie.log


echo " - > Done\n"
echo "Setting rights\n"
chown -R www-data:www-data /var/cache/autonomie/
chmod -R o-rwx /var/cache/autonomie/

chown -R www-data:www-data *
chmod -R o-rwx *
echo " - > Done\n"

echo "Installation is done, you need to\n"
echo " 1- Configure some stuff in ${WWW_DIR}/autonomie/production.ini\n"
echo " 2- Setup the apache stuff\n"
exit 1
