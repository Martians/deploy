#!/bin/sh

###################################################################################################
echo "system: stop firewalld and selinux"
sudo systemctl stop firewalld.service
sudo systemctl disable firewalld.service
sudo setenforce 0
sudo sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config


###################################################################################################
echo "system: copy ssh key"
sudo mkdir -p /root/.ssh
sudo rm /root/.ssh/* -rf
sudo cp /vagrant/config/.ssh/* /root/.ssh -rf

sudo chmod 700 /root/.ssh
sudo chmod 600 -R /root/.ssh/ 

:<<'COMMENT'
sudo mkdir -p /home/vagrant/.ssh
sudo rm /home/vagrant/.ssh/* -rf
sudo cp /vagrant/config/.ssh/* /home/vagrant/.ssh -rf

sudo chmod 700 /home/vagrant/.ssh
sudo chmod 600 -R /home/vagrant/.ssh/ 
sudo chown vagrant:vagrant -R /home/vagrant/.ssh
COMMENT