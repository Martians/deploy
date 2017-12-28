#!/bin/sh
sudo yum install -y ntp ntpdate

echo "repo: config ntp server"
sudo sh -c "echo 'SYNC_HWCLOCK=yes' >>/etc/sysconfig/ntpd"
sudo sed -i "/restrict default/s/.*/restrict default nomodify/g" /etc/ntp.conf
sudo sed -i "/server 3/a\ \nserver  127.127.1.0\nfudge   127.127.1.0 stratum 10" /etc/ntp.conf
sudo cat /etc/ntp.conf

echo "repo: ntp completed"
echo 
