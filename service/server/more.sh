#!/bin/sh

BASE=$(cd "$(dirname "$0")"; cd ..; pwd)
cd $BASE

$BASE/server/sshd.sh $@

echo "------------------------"
docker exec -it host1 /bin/bash