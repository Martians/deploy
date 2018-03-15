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
    DocumentRoot "$REPO_DST"
    <Directory "$REPO_DST">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
      </Directory>
</VirtualHost>
EOF

mkdir $REPO_DST -p

work_output "http completed!"
echo  