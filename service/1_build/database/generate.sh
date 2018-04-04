#!/bin/bash

<<'COMMENT'
COMMENT

TABLE=csv_db
SOURCE=/source/system

#######################################################################
BASE_PATH=$(cd "$(dirname "$0")"; cd ../..; pwd)
cd $BASE_PATH

. 0_config/config.sh

#rm /etc/httpd/conf.d/local.conf -rf
if [ $(set_file_flag /installed) -eq 1 ]; then
	echo "already install, just start"
	systemctl start mariadb
	systemctl start httpd
	exit
fi

#######################################################################
PORT=808
BASE=/generate

sudo cp -f /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.save

echo "exact data"
tar -zxvf $SOURCE/benkeen-generatedata-3.2.8-1-ga5d6fea.tar.gz -C /
mv /benkeen-generatedata* $BASE

# for apache user create settings.php in such dir
chmod 777 $BASE
chmod 777 /$BASE/cache

#######################################################################
yum -y install mariadb mariadb-server
yum -y install httpd php php-mysql

echo "start mariadb"
systemctl start mariadb
sleep 1

PASSWD=111111
echo "initial mariadb"
mysql_secure_installation <<EOF

y
$PASSWD
$PASSWD
n
n
y
y
EOF

# create table
echo "create database $TABLE; show databases; \q;" | mysql -u root -p$PASSWD

#######################################################################
# keep config in settings.php; remove settings.php and will reconfigur
#rm $BASE/settings.example.php $BASE/settings.php  

cat << EOF | sudo tee -a /etc/httpd/conf.d/generate.conf
<VirtualHost *:$PORT>
    DocumentRoot "$BASE"
    <Directory "$BASE">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
      </Directory>
</VirtualHost>
EOF

echo "listen port $PORT"
sed -i "/Listen 80/a\Listen $PORT" /etc/httpd/conf/httpd.conf

<<'COMMENT'
echo "
#IncludeOptional conf.d/php.conf 
" >> /etc/httpd/conf/httpd.conf
COMMENT

echo "start httpd"
systemctl restart httpd


#grant select,insert,update,delete,create,drop privileges on csv_db.* to root@localhost identified by '111111';
#######################################################################
set_file_flag /installed 1