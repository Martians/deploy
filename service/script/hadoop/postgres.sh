#!/bin/bash
# http://blog.csdn.net/pugu12/article/details/51241174

echo 'install postgres'
yum install -y postgresql95-server.x86_64 postgresql95-contrib.x86_64

echo 'config postgres enviroment'
cat << EOF > /var/lib/pgsql/.pgsql_profile
export PGDATA=/var/lib/pgsql/9.5/data
export PATH=\$PATH:/usr/pgsql-9.5/bin
EOF

###########################################################################################
echo "initial mariadb"
su - postgres <<EOF
#source ~/.bash_profile

source /var/lib/pgsql/.pgsql_profile 
rm /var/lib/pgsql/9.5/data -rf
echo "111111" > /tmp/pwfile

#initdb -U postgres -W 
initdb -U postgres --pwfile /tmp/pwfile
EOF

echo 'config and PG'
\cp /var/lib/pgsql/9.5/data/postgresql.conf /var/lib/pgsql/9.5/data/postgresql.conf.save -rf
sed -i "/#listen_addresses/i\listen_addresses = '*'" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i "/#listen_addresses/i\port = 5432" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i '/# IPv6 local connections:/i host    all             all             0.0.0.0/0               md5' /var/lib/pgsql/9.5/data/pg_hba.conf

<<'COMMENT'
echo "pg database start test"
pg_ctl start -D /var/lib/pgsql/9.5/data/
echo "wait postgres start ..."
sleep 3

psql -U postgres
\q
pg_ctl stop
COMMENT

###########################################################################################

echo "config hive in postgres"
systemctl enable postgresql-9.5.service
systemctl restart postgresql-9.5.service