#!/bin/sh

WORK=/mnt/disk
BASE=$(cd "$(dirname "$0")"; cd ..; pwd)

#echo local path: $LOCAL
#echo "export PATH=\$PATH:$LOCAL" >> ~/.bashrc

echo "$BASE/server/sshd.sh"  > $WORK/sshd.sh
echo "$BASE/server/host.sh"  > $WORK/host.sh

