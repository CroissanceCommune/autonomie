#!/bin/bash

set -x

sudo apt-get --reinstall install -qq language-pack-en language-pack-fr

echo "USE mysql;\nUPDATE user SET password=PASSWORD('autonomie') WHERE user='autonomie';\nFLUSH PRIVILEGES;\n" | mysql -u root
echo "create database autonomie;\ngrant all privileges on autonomie.* to autonomie@localhost identified by 'autonomie';\nFLUSH PRIVILEGES;\n" | mysql -u root
