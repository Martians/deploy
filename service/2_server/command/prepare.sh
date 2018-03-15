#!/bin/bash

WORK=/mnt/disk
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)

#echo local path: $HOST_LOCAL
#echo "export PATH=\$PATH:$HOST_LOCAL" >> ~/.bashrc

# echo "$BASE/server/sshd.sh"  > $WORK/sshd.sh
# echo "$BASE/server/host.sh"  > $WORK/host.sh

$BASE/server/proxy.sh
$BASE/server/http.sh

