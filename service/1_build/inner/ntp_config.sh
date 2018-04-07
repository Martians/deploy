#!/bin/bash

BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

LOCAL_SERVER="server $HOST_NTP prefer"
grep -q "$LOCAL_SERVER" /etc/ntp.conf
if [ $? -eq 0 ]; then
	# echo "already set ntp"
	exit
fi

echo "set ntp client"
sudo yum install -y ntp ntpdate

sudo sh -c "echo 'SYNC_HWCLOCK=yes' >>/etc/sysconfig/ntpd"
sudo sed -i 's/\(server [0-3]\)/# \1/g' /etc/ntp.conf
sudo sed -i "/server 0/i$LOCAL_SERVER" /etc/ntp.conf
sudo sed -i "/server 3/a\ \nserver  127.127.1.0\nfudge   127.127.1.0 stratum 10" /etc/ntp.conf
