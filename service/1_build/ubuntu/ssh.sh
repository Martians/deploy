#!/bin/bash

##############################################################################
# BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
# cd $BASE_PATH

# . 0_config/config.sh
##############################################################################
cp /docker/1_build/server/start_sshd.sh /start.sh
mkdir -p /var/run/sshd

apt-get install -y openssh-client openssh-server
echo "root:111111" | chpasswd

#####################################################################
echo "sshd config"
sed -i 's/UsePAM yes/#UsePAM yes/g' /etc/ssh/sshd_config
sed -i 's/#UsePAM no/UsePAM no/g' /etc/ssh/sshd_config
sed -i 's/#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#UseDNS yes/UseDNS no/g' /etc/ssh/sshd_config
sed -i 's/^GSSAPIAuthentication yes/GSSAPIAuthentication no/g' /etc/ssh/sshd_config
sed -i "s/.*\(PermitRootLogin \).*/\1yes/" /etc/ssh/sshd_config

# ssh-keygen -t rsa -f /etc/ssh/ssh_host_rsa_key -N ''
# ssh-keygen -t dsa -f /etc/ssh/ssh_host_dsa_key -N ''
# ssh-keygen -t ecdsa -f /etc/ssh/ssh_host_ecdsa_key -N ''
# ssh-keygen -t ed25519 -f /etc/ssh/ssh_host_ed25519_key -N ''

mkdir -p /root/.ssh/
cd /root/.ssh
# ssh-keygen -t rsa -N ''

echo "StrictHostKeyChecking=no" > /root/.ssh/config
echo "UserKnownHostsFile=/dev/null" >> /root/.ssh/config


