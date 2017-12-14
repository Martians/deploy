#!/bin/sh

echo 'set locale timezone ...'
sudo localectl set-locale LANG=en_US.utf8
sudo timedatectl set-timezone Asia/Shanghai

echo 'copy vagrant .ssh'
sudo mkdir -p /root/.ssh;
sudo chmod 600 /root/.ssh;
sudo cp /home/vagrant/.ssh/authorized_keys /root/.ssh/

