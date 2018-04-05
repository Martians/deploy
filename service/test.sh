#!/bin/sh

BASE_PATH=$(cd "$(dirname "$0")"; pwd)
cd $BASE_PATH

. 0_config/config.sh

# dns_add work 192.168.3.2
# dns_reload

# dig +short @127.0.0.1 work.data.com 
# dig +short @127.0.0.1 -x 192.168.3.5
