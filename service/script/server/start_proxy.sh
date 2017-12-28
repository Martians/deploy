#!/bin/sh

echo "start proxy"
/etc/init.d/apt-cacher-ng start
tail -f /var/log/apt-cacher-ng/*

