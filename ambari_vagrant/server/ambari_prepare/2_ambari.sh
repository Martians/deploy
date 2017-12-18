#!/bin/sh
###########################################################################################
echo 'install postgres'
yum install -y postgresql95-server.x86_64 postgresql95-contrib.x86_64
echo 'install complete, press any key ...'
read

echo 'config postgres enviroment'
cat << EOF > /var/lib/pgsql/.pgsql_profile
export PGDATA=/var/lib/pgsql/9.5/data
export PATH=\$PATH:/usr/pgsql-9.5/bin
EOF

echo 'initialize postgres with user postgres'
su postgres