#!/bin/sh

source /vagrant/server/ambari_prepare/move_ambari_config.sh

####################################################################
echo "stop ambari-agent"
sudo ambari-agent stop

echo "clear ambari-agent keys"
sudo rm /var/lib/ambari-agent/keys/* 

echo "update ambari-server url"
sudo sed -i "/hostname/s/=\(.*\)/=$MOVE_HOST/g" /etc/ambari-agent/conf/ambari-agent.ini

####################################################################
echo "start ambari-agent"
sudo ambari-agent start