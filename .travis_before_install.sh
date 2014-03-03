#!/bin/bash

set -x

sudo apt-get update -qq
sudo apt-get --reinstall install -qq language-pack-en language-pack-fr
sudo easy_install distribute==0.6.28
export TZ="Europe/Paris"
sudo apt-get install -qq libjpeg8 libjpeg8-dev libfreetype6 libfreetype6-dev zlib1g-dev tree
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so.8 ~/virtualenv/python2.7/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so ~/virtualenv/python2.7/lib/
sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so ~/virtualenv/python2.7/lib/

echo "USE mysql;\nUPDATE user SET password=PASSWORD('autonomie') WHERE user='autonomie';\nFLUSH PRIVILEGES;\n" | mysql -u root
echo "create database autonomie;\ngrant all privileges on autonomie.* to autonomie@localhost identified by 'autonomie';\nFLUSH PRIVILEGES;\n" | mysql -u root
