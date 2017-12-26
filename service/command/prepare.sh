#!/bin/sh

BASE=/mnt/disk
LOCAL=$(cd "$(dirname "$0")"; pwd)

echo local path: $LOCAL
echo "export PATH=\$PATH:$LOCAL" >> ~/.bashrc

echo "$LOCAL/create.sh" > $BASE/create.sh
echo "$LOCAL/start.sh"  > $BASE/start.sh

