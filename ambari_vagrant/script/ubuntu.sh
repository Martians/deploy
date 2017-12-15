#!/bin/sh

echo "disable firewall"
sudo ufw disable

sudo mv /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /vagrant/config/repo/*.list /etc/apt/sources.list

sudo apt-get clean
sudo apt-get update

