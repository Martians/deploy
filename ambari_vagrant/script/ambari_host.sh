#!/bin/sh

source /vagrant/config/config.sh
source /vagrant/script/vagrant.sh

echo "set yum proxy address" 
sudo sed -i "/cachedir/a\proxy=http://$PROXY_HOST:3142" /etc/yum.conf

source /vagrant/script/system.sh


##############################################################################################
#dns config
echo 'modify dns config'
sudo sed -i "/plugins/a\dns=none" /etc/NetworkManager/NetworkManager.conf 
sudo sed -i "/nameserver/d" /etc/resolv.conf

sudo sh -c "echo '
search $DOMAIN
nameserver $REPO_HOST
nameserver $PUBLIC_DNS
'>> /etc/resolv.conf"
sudo systemctl restart NetworkManager.service

dig repo.$DOMAIN



##############################################################################################
echo "set ntp client"
sudo yum install -y ntp ntpdate

sudo sh -c "echo 'SYNC_HWCLOCK=yes' >>/etc/sysconfig/ntpd"
sudo sed -i 's/\(server [0-3]\)/# \1/g' /etc/ntp.conf
sudo sed -i "/server 0/i\server $REPO_HOST prefer" /etc/ntp.conf
sudo sed -i "/server 3/a\ \nserver  127.127.1.0\nfudge   127.127.1.0 stratum 10" /etc/ntp.conf

sudo systemctl restart ntpd.service
sudo systemctl enable ntpd.service




