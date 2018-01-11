#!/bin/sh

echo "======== [yum update repos list]"
sudo mkdir /etc/yum.repos.d/save -p
sudo mv /etc/yum.repos.d/CentOS* /etc/yum.repos.d/save
sudo cp /vagrant/config/repo/*.repo /etc/yum.repos.d/

sudo sed -i "/gpgcheck/s/1/0/" /etc/yum.repos.d/CentOS7-*.repo
sudo sed -i "/gpgcheck/a\priority=2" /etc/yum.repos.d/CentOS7-*.repo
