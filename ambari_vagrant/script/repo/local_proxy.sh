#!/bin/sh
source /vagrant/config/config.sh

PROXY_LOCAL=proxy.$DOMAIN
#PROXY_LOCAL=$PROXY_HOST

echo "set yum proxy address" 
sudo sed -i "/cachedir/a\proxy=http://$PROXY_LOCAL:3142" /etc/yum.conf
