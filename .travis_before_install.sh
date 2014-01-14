#!/bin/bash

set -x

sudo apt-get update -qq
sudo apt-get install -qq build-essential libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev python-imaging
sudo apt-get --reinstall install -qq language-pack-en language-pack-fr
export TZ="Europe/Paris"

echo "USE mysql;\nUPDATE user SET password=PASSWORD('autonomie') WHERE user='autonomie';\nFLUSH PRIVILEGES;\n" | mysql -u root
echo "create database autonomie;\ngrant all privileges on autonomie.* to autonomie@localhost identified by 'autonomie';\nFLUSH PRIVILEGES;\n" | mysql -u root
