echo 'INSTALL NAMED TOOLS'
yum install -y bind-utils

echo 'DNS CHECK'
host -t NS bigdata.wh.com 192.168.36.239
host -t A dns.bigdata.wh.com 192.168.36.239

echo 'INSTALL PG'
yum install -y postgresql95-server.x86_64
yum install -y postgresql95-contrib.x86_64

echo 'CONFIG PG DATA'
cat << 'eof' > /var/lib/pgsql/.bash_profile
[ -f /etc/profile ] && source /etc/profile
PGDATA=/var/lib/pgsql/9.5/data
export PGDATA
# If you want to customize your settings,
# Use the file below. This is not overridden
# by the RPMS.
[ -f /var/lib/pgsql/.pgsql_profile ] && source /var/lib/pgsql/.pgsql_profile
eof

echo 'CONFIG PG PATH'
cat << 'eof' > /var/lib/pgsql/.pgsql_profile
export PATH=$PATH:/usr/pgsql-9.5/bin/
eof

echo 'INIT AND CONFIG PG'
source .bash_profile
initdb -U postgres -W
sed -i -e '/^#listen_addresses =/s/^#//' -e '/^#port =/s/^#//' -e "/listen_addresses =.*/s@=.*@= '*'@" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i '/# IPv6 local connections:/i host    all             all             0.0.0.0/0               md5' /var/lib/pgsql/9.5/data/pg_hba.conf

echo 'START PG'
pg_ctl start -D /var/lib/pgsql/9.5/data/
ss -tpnl |grep 5432
psql -U postgres
pg_ctl stop


echo 'ENABLE PG SERVICE'
systemctl enable postgresql-9.5.service
systemctl start postgresql-9.5.service


echo 'CREATE AMBARI DATABASE'
sudo -u postgres psql
CREATE DATABASE ambari;
CREATE USER ambari WITH PASSWORD '123';
GRANT ALL PRIVILEGES ON DATABASE ambari TO ambari;

\c ambari
CREATE SCHEMA ambari AUTHORIZATION ambari;
ALTER SCHEMA ambari OWNER TO ambari;
ALTER ROLE ambari SET search_path to 'ambari', 'public';
\q

echo 'INIT AMBARI DATABASE SHCEMA'
psql -U ambari -d ambari
\i /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql
\d

echo 'SETUP AMBARI SERVER'
scp vagrant@repo.bigdata.wh.com:/home/repo/resource/jdk-8u112-linux-x64.tar.gz /var/lib/ambari-server/resources/
scp vagrant@repo.bigdata.wh.com:/home/repo/resource/jce_policy-8.zip /var/lib/ambari-server/resources/

ambari-server setup
Customize user account for ambari-server daemon [y/n] (n)? n
JDK Enter choice (1): 1
Enter advanced database configuration [y/n] (n)? y
database options Enter choice (1): 4
Hostname (localhost): hdp.bigdata.wh.com
Port (5432): 
Database name (ambari):
Postgres schema (ambari):
Username (ambari):
Enter Database Password (bigdata):123
Proceed with configuring remote database connection properties [y/n] (y)? y

echo 'START AMBARI SERVER'
ambari-server start

echo 'CUSLER'
http://repo.bigdata.wh.com/component/HDP/centos7/2.x/updates/2.6.1.0/
http://repo.bigdata.wh.com/component/HDP-UTILS-1.1.0.21/centos7/


echo 'CREATE HIVE DATABASE'
sudo -u postgres psql
CREATE DATABASE hive;
CREATE USER hive WITH PASSWORD '123';
GRANT ALL PRIVILEGES ON DATABASE hive TO hive;

\c hive
CREATE SCHEMA hive AUTHORIZATION hive;
ALTER SCHEMA hive OWNER TO hive;
ALTER ROLE hive SET search_path to 'hive', 'public';
\q

echo 'CONFIG JDBC'
scp vagrant@repo.bigdata.wh.com:/home/repo/resource/postgresql-jdbc.jar /root/
ambari-server setup --jdbc-db=postgres --jdbc-driver=/root/postgresql-jdbc.jar
