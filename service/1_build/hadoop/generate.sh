#!/bin/bash

<<'COMMENT'
COMMENT

TABLE=csv_db
SOURCE=/source/system
CHECK_FILE=/executed
#######################################################################

#rm /etc/httpd/conf.d/local.conf -rf
if [ -f $CHECK_FILE ] && [ `more $CHECK_FILE` -eq 1 ]; then
	echo "already install, just start"
	systemctl start mariadb
	systemctl start httpd
	exit
fi
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
PORT=808
HOME=/generate

sudo cp -f /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.save

echo "exact data"
tar -zxvf $SOURCE/benkeen-generatedata-3.2.8-1-ga5d6fea.tar.gz -C /
mv benkeen-generatedata-a5d6fea $HOME

# for apache user create settings.php in such dir
chmod 777 $HOME
chmod 777 /$HOME/cache

# keep config in settings.php; remove settings.php and will reconfigure
#rm $HOME/settings.example.php $HOME/settings.php  

cat << EOF | sudo tee -a /etc/httpd/conf.d/generate.conf
<VirtualHost *:$PORT>
    DocumentRoot "$HOME"
    <Directory "$HOME">
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

echo 1 > $CHECK_FILE