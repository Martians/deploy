#!/bin/bash

# 根据外部配置，自动获取ip
HOST_REPO=$(alloc_host REPO)
HOST_PROXY=$(alloc_host PROXY)
HOST1_HOST=$(alloc_host 1)
HOST2_HOST=$(alloc_host 2)
HOST3_HOST=$(alloc_host 3)

# 得到ip的反向位置
DNS_ARPA=$(echo $HOST_LOCAL | awk -F"." '{ print $2"."$1 }')

# no use now
# PUBLIC_DNS=$HOST_DNS_PUBLIC

# echo "  DNS_ARPA: $DNS_ARPA"
# echo "  HOST_REPO_LAST: $(host_reverse REPO)"
# echo "  HOST_PROXY_LAST: $(host_reverse PROXY)"
# echo "  PUBLIC_DNS: $HOST_DNS_PUBLIC"

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
#sudo cat /var/named/$DOMAIN

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

$(host_reverse REPO)    IN   PTR  repo.$DOMAIN.
$(host_reverse PROXY)   IN   PTR  proxy.$DOMAIN.
$(host_reverse 1)       IN   PTR  host1.$DOMAIN.
$(host_reverse 2)       IN   PTR  host2.$DOMAIN.
$(host_reverse 3)       IN   PTR  host3.$DOMAIN.
EOF
#sudo cat /var/named/$DOMAIN.arpa

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

# 生成控制秘钥，以便在不重启服务的情况下更新配置
# rndc-confgen -a