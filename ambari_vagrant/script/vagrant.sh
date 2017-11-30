
#!/usr/bin/env bash

# vagrant initialize
source config.sh

# timezone config
echo 'modify lang and timezone'
sudo localectl set-locale LANG=en_US.utf8
sudo timedatectl set-timezone Asia/Shanghai

# copy vagrant ssh config
echo 'modify lang and timezone'
sudo mkdir -p /root/.ssh; 
sudo chmod 600 /root/.ssh; 
sudo cp /home/vagrant/.ssh/authorized_keys /root/.ssh/

