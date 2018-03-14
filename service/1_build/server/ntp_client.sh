#!/bin/bash
BASE=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE

source $BASE/script/config.sh

echo "set ntp client"
sudo yum install -y ntp ntpdate

sudo sh -c "echo 'SYNC_HWCLOCK=yes' >>/etc/sysconfig/ntpd"
sudo sed -i 's/\(server [0-3]\)/# \1/g' /etc/ntp.conf
sudo sed -i "/server 0/i\server $LOCAL prefer" /etc/ntp.conf
sudo sed -i "/server 3/a\ \nserver  127.127.1.0\nfudge   127.127.1.0 stratum 10" /etc/ntp.conf
