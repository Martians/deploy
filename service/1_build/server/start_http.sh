#!/bin/bash

echo "start httpd ... [`date`]"

#mkdir -p /run/httpd

for count in {1..5}  
do  
	echo "start $count"
	httpd -DFOREGROUND
	sleep 1
done  

#tail -f /var/log/httpd/*
