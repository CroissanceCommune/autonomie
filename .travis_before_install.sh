#!/bin/bash


sudo apt-get --reinstall install -qq language-pack-en language-pack-fr

mysql --user travis --password='' --database=$MYSQL_DBNAME << END_SQL
create database egw;
grant all privileges on egw.* to egw@localhost identified by "egw";
flush privileges;
END_SQL
