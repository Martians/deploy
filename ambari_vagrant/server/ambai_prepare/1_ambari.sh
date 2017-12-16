#!/bin/sh

###########################################################################################
source /vagrant/config/config.sh
ssh host1.$DOMAIN
ssh host2.$DOMAIN
ssh host3.$DOMAIN