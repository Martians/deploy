#!/bin/sh

HOME=/html

#install http file service
echo "install http server"
sudo yum install -y httpd

echo "config http server"
## move welcome.conf, so we can't get file service directly
sudo cp -f /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.save

## create virtual server
sudo rm /etc/httpd/conf.d/local.conf -rf
cat << EOF | sudo tee -a /etc/httpd/conf.d/local.conf
<VirtualHost *:80>
    DocumentRoot "$HOME"
    <Directory "$HOME">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
      </Directory>
</VirtualHost>
EOF

mkdir /var/log/httpd -p 
mkdir $HOME -p

ls /var/log/httpd -la
echo "http completed!"
echo 