#!/bin/bash

set -x

sudo apt-get --reinstall install -qq language-pack-en language-pack-fr

mysql -e 'create database egw;'
mysql -e 'grant all privileges on egw.* to egw@localhost identified by "egw";'
