#!/bin/sh


echo "proxy: install apt-cacher-ng"
sudo apt-get install -y apt-cacher-ng curl

echo "proxy: download centos mirror list"
curl https://www.centos.org/download/full-mirrorlist.csv | sed 's/^.*"http:/http:/' | sed 's/".*$//' | grep ^http > centos_mirrors
sudo mv centos_mirrors /usr/lib/apt-cacher-ng/centos_mirrors

echo "proxy: update proxy config"
sudo sed -i "s/[# \t]*\(VerboseLog: \).*$/\11/" /etc/apt-cacher-ng/acng.conf
sudo sed -i "/Remap-debrep/i\Remap-centos: file:centos_mirrors \/centos; mirrors.163.com\/centos mirrors.aliyun.com\/centos\n" /etc/apt-cacher-ng/acng.conf
# ExTreshold: 4

echo "check at http://127.0.0.1:3142"
echo "cd /var/cache/apt-cacher-ng"
echo "proxy: completed"
