#!/bin/sh


echo 'install postgres'
yum install -y postgresql95-server.x86_64 postgresql95-contrib.x86_64

echo 'config postgres enviroment'
cat << EOF > /var/lib/pgsql/.pgsql_profile
export PGDATA=/var/lib/pgsql/9.5/data
export PATH=\$PATH:/usr/pgsql-9.5/bin
EOF
source ~/.bash_profile


exit


export PATH=\$PATH:/usr/pgsql-9.5/bin
su postgres
psql -U postgres  <<EOF

y
$PASSWD
$PASSWD
n
n
y
y
EOF



initdb -U postgres -W
echo 'initialize complete, press any key ...'
read

###########################################################################################
echo 'config and PG'
\cp /var/lib/pgsql/9.5/data/postgresql.conf /var/lib/pgsql/9.5/data/postgresql.conf.save -rf
sed -i "/#listen_addresses/i\listen_addresses = '*'" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i "/#listen_addresses/i\port = 5432" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i '/# IPv6 local connections:/i host    all             all             0.0.0.0/0               md5' /var/lib/pgsql/9.5/data/pg_hba.conf

echo "pg database start test"
pg_ctl start -D /var/lib/pgsql/9.5/data/
echo "wait postgres start ..."
sleep 3

psql -U postgres
\q
pg_ctl stop



CREATE DATABASE hive;
CREATE USER hive WITH PASSWORD '1';
GRANT ALL PRIVILEGES ON DATABASE hive TO hive;

\c hive
CREATE SCHEMA hive AUTHORIZATION hive;
ALTER SCHEMA hive OWNER TO hive;
ALTER ROLE hive SET search_path to 'hive', 'public';

psql -U hive -d hive

