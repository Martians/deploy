#!/bin/sh

echo "copy and execute, not directly"
read

###########################################################################################
echo 'CREATE AMBARI DATABASE'
sudo -u postgres psql
CREATE DATABASE ambari;
CREATE USER ambari WITH PASSWORD 'bigdata';
GRANT ALL PRIVILEGES ON DATABASE ambari TO ambari;
\c ambari
CREATE SCHEMA ambari AUTHORIZATION ambari;
ALTER SCHEMA ambari OWNER TO ambari;
ALTER ROLE ambari SET search_path to 'ambari', 'public';
\q

echo 'CREATE HIVE DATABASE'
sudo -u postgres psql
CREATE DATABASE hive;
CREATE USER hive WITH PASSWORD 'bigdata';
GRANT ALL PRIVILEGES ON DATABASE hive TO hive;
\c hive
CREATE SCHEMA hive AUTHORIZATION hive;
ALTER SCHEMA hive OWNER TO hive;
ALTER ROLE hive SET search_path to 'hive', 'public';
\q

echo 'CREATE RANGER DATABASE'
sudo -u postgres psql
CREATE DATABASE ranger;
CREATE USER ranger WITH PASSWORD 'bigdata';
GRANT ALL PRIVILEGES ON DATABASE ranger TO ranger;
\c ranger
CREATE SCHEMA ranger AUTHORIZATION ranger;
ALTER SCHEMA ranger OWNER TO ranger;
ALTER ROLE ranger SET search_path to 'ranger', 'public';
\q

###########################################################################################
echo 'INIT AMBARI DATABASE SHCEMA'
psql -U ambari -d ambari
\i /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql
\d
\q
\q
