#!/bin/bash

set -x

sudo apt-get --reinstall install -qq language-pack-en language-pack-fr

echo "USE mysql;\nUPDATE user SET password=PASSWORD('egw') WHERE user='egw';\nFLUSH PRIVILEGES;\n" | mysql -u root
echo "create database egw;\ngrant all privileges on egw.* to egw@localhost identified by 'egw';\nFLUSH PRIVILEGES;\n" | mysql -u root
