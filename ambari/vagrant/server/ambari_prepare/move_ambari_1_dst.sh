#!/bin/sh
source /vagrant/server/ambari_prepare/move_ambari_config.sh

####################################################################
echo "wait to execute
	0_ambari.sh
	2_ambari.sh
	3_ambari.sh
	4_ambari.sh
press any key to continue ..."
read

###########################################################################################
echo 'CREATE AMBARI DATABASE'
echo "copy and execute 
=========================================
CREATE DATABASE ambari;
CREATE USER ambari WITH PASSWORD 'bigdata';
GRANT ALL PRIVILEGES ON DATABASE ambari TO ambari;
\c ambari
CREATE SCHEMA ambari AUTHORIZATION ambari;
ALTER SCHEMA ambari OWNER TO ambari;
ALTER ROLE ambari SET search_path to 'ambari', 'public';
\q
========================================="
sudo -u postgres psql

####################################################################
echo 'COPY JDK AND JCE'
scp root@repo.$DOMAIN:/vagrant/repo/resource/jdk-8u112-linux-x64.tar.gz /var/lib/ambari-server/resources/
scp root@repo.$DOMAIN:/vagrant/repo/resource/jce_policy-8.zip /var/lib/ambari-server/resources/

echo 'CONFIG JDBC'
scp root@repo.$DOMAIN:/vagrant/repo/resource/postgresql-jdbc.jar /root/

echo "ambari setup"
ambari-server setup --/=postgres --jdbc-driver=/root/postgresql-jdbc.jar
ambari-server setup

###########################################################################################
echo "copy and execute 
=========================================
sudo -u postgres psql
drop database ambari;
create database ambari;
\q
========================================="

echo "load ambari sql"
psql -U postgres -d ambari -f /tmp/ambari.sql 

###########################################################################################
echo "try to start ambari-server, press any key ..."
read
ambari-server start
