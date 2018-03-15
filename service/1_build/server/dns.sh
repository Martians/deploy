#!/bin/bash

DOMAIN="data.com"
NETMASK="255.255.254.0"
GATEWAY="192.168.37.254"

HOST_REPO="192.168.37.198"
HOST_PROXY="192.168.37.199"

TEST_HOST="192.168.37.200"

HOST1_HOST="192.168.37.191"
HOST2_HOST="192.168.37.192"
HOST3_HOST="192.168.37.193"


DNS_ARPA=168.192
HOST_REPO_LAST=198.37
HOST_PROXY_LAST=199.37
PUBLIC_DNS=192.168.30.1

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
ns      IN   A   $HOST_REPO

repo    IN   A   $HOST_REPO
proxy   IN   A   $HOST_PROXY
host1   IN   A   $HOST1_HOST
host2   IN   A   $HOST2_HOST
host3   IN   A   $HOST3_HOST
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
ns      IN    A   $HOST_REPO

$HOST_REPO_LAST    IN   PTR  repo.$DOMAIN.
$HOST_PROXY_LAST   IN   PTR  proxy.$DOMAIN.
HOST1_HOST    IN   PTR  host1.$DOMAIN.
HOST2_HOST    IN   PTR  host2.$DOMAIN.
HOST3_HOST    IN   PTR  host3.$DOMAIN.
EOF
sudo cat /var/named/$DOMAIN.arpa

<<'COMMENT'
sudo systemctl restart named.service
sudo systemctl enable named.service

echo "repo: dns query - repo.$DOMAIN:"
dig +short @$HOST_REPO repo.$DOMAIN 

echo "repo: dns ptr - $HOST_REPO:"
dig +short @$HOST_REPO -x $HOST_REPO 

echo "repo: dns soa - repo.$DOMAIN:"
dig @$HOST_REPO soa repo.$DOMAIN 

echo "repo: dns completed"
echo 
COMMENT