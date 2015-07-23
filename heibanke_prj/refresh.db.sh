#!/bin/bash
/usr/local/mysql/bin/mysql -u root -p<<eof
drop database if exists heibanke;
CREATE DATABASE heibanke DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
eof
python ./manage.py migrate
