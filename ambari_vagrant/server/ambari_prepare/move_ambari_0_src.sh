#!/bin/sh
source /vagrant/server/ambari_prepare/move_ambari_config.sh

####################################################################
echo "stop ambari server"
ambari-server stop

echo "move to backup dir"
mkdir /tmp/dbdumps/
cd /tmp/dbdumps/

echo "dump ambari sql"
pg_dump -U ambari -f ambari.sql

echo "copy ambari.sql to host"
scp /tmp/dbdumps/ambari.sql $MOVE_HOST:/tmp/

## echo "ambari backup"
## ambari-server backup