#!/bin/sh
source /vagrant/config/config.sh

#<<'COMMENT'
#COMMENT

##################################################################################################
#install http file service
echo "repo: install http server"
sudo yum install -y httpd

echo "repo: config http server"
## move welcome.conf, so we can't get file service directly
sudo cp -f /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.bak
sudo mv /etc/httpd/conf.d/welcome.conf /etc/httpd/conf.d/welcome.conf.save

## create virtual server
sudo rm /etc/httpd/conf.d/local.conf -rf
cat << EOF | sudo tee -a /etc/httpd/conf.d/local.conf
<VirtualHost *:80>
    DocumentRoot "/vagrant/repo"
    <Directory "/vagrant/repo">
        Options Indexes FollowSymLinks
        AllowOverride None
        Require all granted
      </Directory>
</VirtualHost>
EOF

sudo systemctl enable httpd
sudo systemctl restart httpd.service
echo "repo: http completed!"
echo 

##################################################################################################
echo "repo: install dns server"
sudo yum install -y bind bind-utils

echo "repo: config dns server"
# /etc/named.conf
sudo cp -f /etc/named.conf /etc/named.conf.bak
sudo sed -i "/listen-on port 53/s/{.*}/{ any; }/g" /etc/named.conf
sudo sed -i "/allow-query/s/{.*}/{ any; }/g" /etc/named.conf

# /etc/named.rfc1912.zones
cat << EOF | sudo tee -a /etc/named.rfc1912.zones
zone "$DOMAIN" IN {
    type master;
    file "$DOMAIN";
    allow-update { none; };
};
zone "$DNS_ARPA.in-addr.arpa" IN {
    type master;
    file "$DOMAIN.arpa";
    allow-update { none; };
};
EOF
sudo cat /etc/named.rfc1912.zones

echo "set domain "
sudo rm /var/named/$DOMAIN -rf
cat << EOF | sudo tee -a /var/named/$DOMAIN
\$TTL 1D
@       IN  SOA  ns.$DOMAIN. root.$DOMAIN. (
        1       ; Serial
        3H      ; Refresh
        5M      ; Retry
        1W      ; Expire
        3H)     ; Negative Cache TTL
;
        IN   NS  ns.$DOMAIN.
ns      IN   A   $REPO_HOST

repo    IN   A   $REPO_HOST
proxy   IN   A   $PROXY_HOST
EOF
sudo cat /var/named/$DOMAIN

echo "set domain ptr"
sudo rm /var/named/$DOMAIN.arpa -rf
cat << EOF | sudo tee -a /var/named/$DOMAIN.arpa
\$TTL 1D
@       IN  SOA  ns.$DOMAIN. root.$DOMAIN. (
        1       ; Serial
        3H      ; Refresh
        5M      ; Retry
        1W      ; Expire
        3H)     ; Negative Cache TTL

@       IN    NS  ns.$DOMAIN.
ns      IN    A   $REPO_HOST

$REPO_HOST_LAST    IN   PTR  repo.$DOMAIN.
$PROXY_HOST_LAST   IN   PTR  proxy.$DOMAIN.
EOF
sudo cat /var/named/$DOMAIN.arpa

sudo systemctl restart named.service
sudo systemctl enable named.service

echo "repo: dns query - repo.$DOMAIN:"
dig +short @$REPO_HOST repo.$DOMAIN 

echo "repo: dns ptr - $REPO_HOST:"
dig +short @$REPO_HOST -x $REPO_HOST 

echo "repo: dns soa - repo.$DOMAIN:"
dig @$REPO_HOST soa repo.$DOMAIN 

echo "repo: dns completed"
echo 

##################################################################################################
echo "repo: install ntp server"

sudo systemctl stop chronyd.service
sudo systemctl disable chronyd.service
sudo yum install -y ntp ntpdate

echo "repo: config ntp server"
sudo sh -c "echo 'SYNC_HWCLOCK=yes' >>/etc/sysconfig/ntpd"
sudo sed -i "/restrict default/s/.*/restrict default nomodify/g" /etc/ntp.conf
sudo sed -i "/server 3/a\ \nserver  127.127.1.0\nfudge   127.127.1.0 stratum 10" /etc/ntp.conf
sudo cat /etc/ntp.conf

sudo systemctl restart ntpd.service
sudo systemctl enable ntpd.service

echo "repo: ntp completed"
echo 

echo 'repo host completed!'