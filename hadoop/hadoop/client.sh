#!/bin/sh

source ./base.sh $@

help_client

echo "enter client:"
docker run -it --rm $CLIENT_INFO $CLIENT_CONFIG $YARN_CLIENT uhopper/hadoop:2.7.2 /bin/bash

