#!/bin/sh

###########################################################################################
echo 'ENABLE PG SERVICE'
systemctl enable postgresql-9.5.service
systemctl restart postgresql-9.5.service
echo 'service restart complete, press any key ...'
read

echo "install ambari"
sudo yum install -y ambari-server.x86_64