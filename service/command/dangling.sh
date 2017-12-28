#!/bin/sh

echo "clear dangling images"
# docker stop $(docker ps -aq)
docker rmi -f $(docker images -q -f dangling=true)
