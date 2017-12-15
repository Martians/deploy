#!/bin/sh

echo 'install postgresql'
yum install -y postgresql95-server.x86_64 postgresql95-contrib.x86_64

echo 'config postgresql enviroment'
cat << EOF > /var/lib/pgsql/.pgsql_profile
export PGDATA=/var/lib/pgsql/9.5/data
export PATH=$PATH:/usr/pgsql-9.5/bin
EOF

echo 'initialize postgresql'
su postgres
source ~/.bash_profile
initdb -U postgres -W

###########################################################################################
echo 'config and PG'
\cp /var/lib/pgsql/9.5/data/postgresql.conf /var/lib/pgsql/9.5/data/postgresql.conf.save -rf
sed -i "/#listen_addresses/i\listen_addresses = '*'" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i "/#listen_addresses/i\port = 5432" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i '/# IPv6 local connections:/i host    all             all             0.0.0.0/0               md5' /var/lib/pgsql/9.5/data/pg_hba.conf

# pg_ctl start -D /var/lib/pgsql/9.5/data/
# psql -U postgres
# \q
# pg_ctl stop
exit
echo 'ENABLE PG SERVICE'
systemctl enable postgresql-9.5.service
systemctl restart postgresql-9.5.service
###########################################################################################


###########################################################################################
echo 'CREATE AMBARI DATABASE'
sudo -u postgres psql
CREATE DATABASE ambari;
CREATE USER ambari WITH PASSWORD '1';
GRANT ALL PRIVILEGES ON DATABASE ambari TO ambari;
\c ambari
CREATE SCHEMA ambari AUTHORIZATION ambari;
ALTER SCHEMA ambari OWNER TO ambari;
ALTER ROLE ambari SET search_path to 'ambari', 'public';
\q

echo 'CREATE HIVE DATABASE'
sudo -u postgres psql
CREATE DATABASE hive;
CREATE USER hive WITH PASSWORD '1';
GRANT ALL PRIVILEGES ON DATABASE hive TO hive;
\c hive
CREATE SCHEMA hive AUTHORIZATION hive;
ALTER SCHEMA hive OWNER TO hive;
ALTER ROLE hive SET search_path to 'hive', 'public';
\q

echo 'CREATE RANGER DATABASE'
sudo -u postgres psql
CREATE DATABASE ranger;
CREATE USER ranger WITH PASSWORD '1';
GRANT ALL PRIVILEGES ON DATABASE ranger TO ranger;
\c ranger
CREATE SCHEMA ranger AUTHORIZATION ranger;
ALTER SCHEMA ranger OWNER TO ranger;
ALTER ROLE ranger SET search_path to 'ranger', 'public';
\q

###########################################################################################
yum install -y ambari-server.x86_64

echo 'INIT AMBARI DATABASE SHCEMA'
psql -U ambari -d ambari
\i /var/lib/ambari-server/resources/Ambari-DDL-Postgres-CREATE.sql
\d

\q


###########################################################################################
source /vagrant/config/config.sh

echo 'COPY JDK AND JCE'
scp root@repo.$DOMAIN:/vagrant/repo/resource/jdk-8u112-linux-x64.tar.gz /var/lib/ambari-server/resources/
scp root@repo.$DOMAIN:/vagrant/repo/resource/jce_policy-8.zip /var/lib/ambari-server/resources/

echo 'CONFIG JDBC'
scp root@repo.$DOMAIN:/vagrant/repo/resource/postgresql-jdbc.jar /root/

echo "ambari setup"
ambari-server setup --jdbc-db=postgres --jdbc-driver=/root/postgresql-jdbc.jar
ambari-server setup

