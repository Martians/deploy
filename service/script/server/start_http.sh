#!/bin/sh

echo "start httpd ... [`date`]"

#mkdir -p /run/httpd

httpd -DFOREGROUND
#tail -f /var/log/httpd/*