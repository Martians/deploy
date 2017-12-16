#!/bin/sh

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
ambari-server start

