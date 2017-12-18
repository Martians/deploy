#!/bin/sh

###########################################################################################

source ~/.bash_profile
initdb -U postgres -W
echo 'initialize complete, press any key ...'
read

###########################################################################################
echo 'config and PG'
\cp /var/lib/pgsql/9.5/data/postgresql.conf /var/lib/pgsql/9.5/data/postgresql.conf.save -rf
sed -i "/#listen_addresses/i\listen_addresses = '*'" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i "/#listen_addresses/i\port = 5432" /var/lib/pgsql/9.5/data/postgresql.conf
sed -i '/# IPv6 local connections:/i host    all             all             0.0.0.0/0               md5' /var/lib/pgsql/9.5/data/pg_hba.conf

pg_ctl start -D /var/lib/pgsql/9.5/data/
psql -U postgres
\q
pg_ctl stop

echo "change to root"
su 