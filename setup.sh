#!/bin/bash

if [ ! -d /root/majerti/autonomie ]
then
    echo "Missing /root/majerti/autonomie, Exiting \n"
    exit 1
fi

if [ ! -d /var/www/autonomie_env ]
then
    echo "Creating virtualenv ... \n"
    virtualenv -- no-site-packages /var/www/autonomie_env
    echo " - > Done\n"
fi

echo "Installing autonomie\n"
source /var/www/autonomie_env/bin/activate

rm -rf /var/www/autonomie_env/autonomie/

mv /root/majerti/autonomie /var/www/autonomie_env/autonomie
cd /var/www/autonomie_env/autonomie
rm -rf .git*
python setup.py develop

/bin/mkdir -p /var/cache/autonomie/beaker
/bin/mkdir -p /var/cache/autonomie/mako

echo " - > Done\n"
echo "Setting rights\n"
chown -R www-data:www-data /var/cache/autonomie/
chmod -R o-rwx /var/cache/autonomie/

chown -R www-data:www-data *
chmod -R o-rwx *
echo " - > Done\n"

echo "Installation is done, you need to\n"
echo " 1- Configure some stuff in /var/www/autonomie_env/autonomie/production.ini\n"
echo " 2- Setup the apache stuff\n"
exit 1
