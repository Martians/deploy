#!/bin/bash

#install http file service
work_output "install http server"
sudo yum install -y httpd

work_output "config http server"
## move welcome.conf, so we can't get file service directly
sudo cp -f /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.save

## create virtual server
sudo rm /etc/httpd/conf.d/local.conf -rf
cat << EOF | sudo tee -a /etc/httpd/conf.d/local.conf
<VirtualHost *:80>
    DocumentRoot "$DOCK_PATH_REPO"
    <Directory "$DOCK_PATH_REPO">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
      </Directory>
</VirtualHost>
EOF

mkdir $DOCK_PATH_REPO -p

work_output "http completed!"
echo  